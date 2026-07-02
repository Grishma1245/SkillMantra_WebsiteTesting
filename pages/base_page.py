"""
base_page.py
------------
Abstract base class for all Page Object classes.

Every Page Object MUST extend BasePage. This class provides reusable, robust
helper methods built on top of Selenium's explicit-wait API (WebDriverWait +
expected_conditions). No time.sleep() is ever used.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import get_timeout
from utils.logger import get_logger

logger = get_logger(__name__)

# Exceptions to retry on during stale-element operations
_STALE_EXCEPTIONS = (StaleElementReferenceException,)


class BasePage:
    """
    Base Page Object providing reusable Selenium interaction helpers.

    All page objects should inherit from this class and access
    ``self.driver`` directly for any driver-level operations not
    covered by the helper methods.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self._timeout = get_timeout()
        self._wait = WebDriverWait(
            driver,
            timeout=self._timeout,
            poll_frequency=0.5,
            ignored_exceptions=_STALE_EXCEPTIONS,
        )

    # ── Private / Internal ─────────────────────────────────────────────────────

    def _wait_for(self, condition, timeout: Optional[int] = None) -> WebElement:
        """Wait for *condition* using the instance's WebDriverWait."""
        wait = self._wait if timeout is None else WebDriverWait(
            self.driver, timeout, poll_frequency=0.5, ignored_exceptions=_STALE_EXCEPTIONS
        )
        return wait.until(condition)

    # ── Element finders ────────────────────────────────────────────────────────

    def wait_for_element(
        self, locator: tuple, timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait until *locator* is present in the DOM and return the element.

        Args:
            locator: A (By.*, 'selector') tuple.
            timeout: Override the default timeout (seconds).

        Returns:
            The found WebElement.

        Raises:
            TimeoutException: If the element is not found within the timeout.
        """
        logger.debug("Waiting for element: %s", locator)
        try:
            return self._wait_for(EC.presence_of_element_located(locator), timeout)
        except TimeoutException:
            logger.error("Element not found within timeout: %s", locator)
            raise

    def wait_for_visible(
        self, locator: tuple, timeout: Optional[int] = None
    ) -> WebElement:
        """Wait until *locator* is visible and return the element."""
        logger.debug("Waiting for element to be visible: %s", locator)
        try:
            return self._wait_for(EC.visibility_of_element_located(locator), timeout)
        except TimeoutException:
            logger.error("Element not visible within timeout: %s", locator)
            raise

    def wait_for_clickable(
        self, locator: tuple, timeout: Optional[int] = None
    ) -> WebElement:
        """Wait until *locator* is clickable and return the element."""
        logger.debug("Waiting for element to be clickable: %s", locator)
        try:
            return self._wait_for(EC.element_to_be_clickable(locator), timeout)
        except TimeoutException:
            logger.error("Element not clickable within timeout: %s", locator)
            raise

    def find_elements(self, locator: tuple) -> List[WebElement]:
        """Return all elements matching *locator* (may be empty list)."""
        return self.driver.find_elements(*locator)

    # ── Core interaction methods ───────────────────────────────────────────────

    def safe_click(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """
        Wait for *locator* to be clickable, scroll it into view, and click it.
        Falls back to JavaScript click if the standard click is intercepted.

        Args:
            locator: A (By.*, 'selector') tuple.
            timeout: Override the default timeout.
        """
        logger.debug("safe_click → %s", locator)
        element = self.wait_for_clickable(locator, timeout)
        self.scroll_into_view(element)
        try:
            element.click()
        except Exception as exc:
            logger.warning(
                "Standard click failed (%s); falling back to JS click for %s", exc, locator
            )
            self.driver.execute_script("arguments[0].click();", element)

    def safe_send_keys(
        self, locator: tuple, text: str, clear_first: bool = True, timeout: Optional[int] = None
    ) -> None:
        """
        Wait for *locator* to be visible, optionally clear it, then type *text*.

        Args:
            locator: A (By.*, 'selector') tuple.
            text: The string to type into the element.
            clear_first: Clear the field before typing (default True).
            timeout: Override the default timeout.
        """
        logger.debug("safe_send_keys → %s | text='%s'", locator, text)
        element = self.wait_for_visible(locator, timeout)
        self.scroll_into_view(element)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def wait_and_get_text(self, locator: tuple, timeout: Optional[int] = None) -> str:
        """
        Wait for *locator* to be visible and return its stripped text content.

        Args:
            locator: A (By.*, 'selector') tuple.
            timeout: Override the default timeout.

        Returns:
            Stripped text of the element.
        """
        element = self.wait_for_visible(locator, timeout)
        text = element.text.strip()
        logger.debug("wait_and_get_text → '%s'", text)
        return text

    # ── Visibility / existence checks ──────────────────────────────────────────

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Return True if *locator* is visible within *timeout* seconds.
        Does NOT raise on TimeoutException — returns False instead.

        Args:
            locator: A (By.*, 'selector') tuple.
            timeout: Max seconds to wait (default 5 for soft checks).

        Returns:
            True if visible; False otherwise.
        """
        try:
            self.wait_for_visible(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """Return True if *locator* exists in the DOM within *timeout* seconds."""
        try:
            self.wait_for_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # ── Scrolling ──────────────────────────────────────────────────────────────

    def scroll_into_view(self, element: WebElement) -> None:
        """Scroll the given element into the visible viewport using JavaScript."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element
        )

    def scroll_to_locator(self, locator: tuple) -> WebElement:
        """
        Wait for *locator* to be present, scroll it into view, and return it.

        Args:
            locator: A (By.*, 'selector') tuple.

        Returns:
            The scrolled-to WebElement.
        """
        element = self.wait_for_element(locator)
        self.scroll_into_view(element)
        return element

    def scroll_to_bottom(self) -> None:
        """Scroll to the very bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open(self, url: str) -> None:
        """Navigate to *url* and log the action."""
        logger.info("Navigating to URL: %s", url)
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Return the browser's current page title."""
        return self.driver.title

    # ── Window / tab management ────────────────────────────────────────────────

    def switch_to_new_tab(self, original_handle: str) -> str:
        """
        Wait for a new browser tab/window to open, switch focus to it,
        and return the new window handle.

        This is needed for the WhatsApp widget which opens api.whatsapp.com
        in a new tab when the chat initialisation button is clicked.

        Args:
            original_handle: The window handle to switch AWAY from.

        Returns:
            The handle of the newly opened window/tab.

        Raises:
            TimeoutException: If no new window appears within the timeout.
        """
        logger.info("Waiting for new browser tab to open...")
        try:
            self._wait_for(EC.number_of_windows_to_be(2))
        except TimeoutException:
            logger.error("No new tab/window opened within %s seconds.", self._timeout)
            raise

        new_handles = [h for h in self.driver.window_handles if h != original_handle]
        if not new_handles:
            raise RuntimeError("Expected a new tab but found none.")

        new_handle = new_handles[0]
        self.driver.switch_to.window(new_handle)
        logger.info("Switched to new tab: %s | URL: %s", new_handle, self.driver.current_url)
        return new_handle

    def switch_back_to_window(self, handle: str) -> None:
        """Switch focus back to the window identified by *handle*."""
        logger.info("Switching back to window handle: %s", handle)
        self.driver.switch_to.window(handle)

    def get_current_window_handle(self) -> str:
        """Return the current active window handle."""
        return self.driver.current_window_handle

    # ── iFrame support ─────────────────────────────────────────────────────────

    def switch_to_iframe(self, locator: tuple) -> None:
        """Wait for the iframe identified by *locator* to be available and switch into it."""
        logger.debug("Switching to iframe: %s", locator)
        self._wait_for(EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_default_content(self) -> None:
        """Switch focus back to the main page content from an iframe."""
        self.driver.switch_to.default_content()

    # ── Attribute / property helpers ───────────────────────────────────────────

    def get_attribute(self, locator: tuple, attribute: str) -> Optional[str]:
        """Return the value of *attribute* for the element at *locator*."""
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    def wait_for_text_in_element(
        self, locator: tuple, text: str, timeout: Optional[int] = None
    ) -> bool:
        """
        Return True when *text* appears inside the element at *locator*.

        Args:
            locator: A (By.*, 'selector') tuple.
            text: Substring to look for.
            timeout: Override default timeout.

        Returns:
            True if text found; raises TimeoutException otherwise.
        """
        logger.debug("Waiting for text '%s' in element %s", text, locator)
        wait = self._wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_url_contains(self, partial_url: str, timeout: Optional[int] = None) -> bool:
        """Wait until the current URL contains *partial_url*."""
        logger.debug("Waiting for URL to contain: %s", partial_url)
        wait = self._wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(partial_url))

    def js_get_inner_text(self, locator: tuple) -> str:
        """Use JavaScript to get innerText of an element (useful for hidden text)."""
        element = self.wait_for_element(locator)
        return self.driver.execute_script("return arguments[0].innerText;", element).strip()

    def count_elements(self, locator: tuple) -> int:
        """Return the count of elements matching *locator* in the DOM."""
        elements = self.find_elements(locator)
        logger.debug("count_elements(%s) → %d", locator, len(elements))
        return len(elements)
