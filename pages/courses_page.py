"""
courses_page.py
---------------
Page Object for the SkillMantra Courses catalog page (https://skillmantraedu.com/courses).

Locators derived from live DOM inspection. The page uses Tailwind CSS utility classes
as primary class-based hooks. Data-driven selectors are kept parameter-friendly.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CoursesPage(BasePage):
    """Page Object for the Courses Catalog page."""

    # ── Page header ────────────────────────────────────────────────────────────
    PAGE_HEADING = (By.CSS_SELECTOR, "section h1, main h1")

    # ── Category filter tabs ───────────────────────────────────────────────────
    # The courses page renders filter tabs; each tab is a <button> with the
    # category name as its text content.
    FILTER_ALL_ECOSYSTEMS     = (By.XPATH, "//button[contains(normalize-space(),'All Ecosystems') or normalize-space()='All']")
    FILTER_SOFTWARE_ENG       = (By.XPATH, "//button[contains(normalize-space(),'Software Engineering')]")
    FILTER_DATA_SCIENCE       = (By.XPATH, "//button[contains(normalize-space(),'Data Science')]")
    FILTER_INFRA_DEVOPS       = (By.XPATH, "//button[contains(normalize-space(),'Infrastructure') or contains(normalize-space(),'DevOps')]")

    # All tab filter buttons together
    ALL_FILTER_TABS = (By.XPATH,
        "//button[contains(normalize-space(),'All Ecosystems') or "
        "         contains(normalize-space(),'Software Engineering') or "
        "         contains(normalize-space(),'Data Science') or "
        "         contains(normalize-space(),'Infrastructure') or "
        "         contains(normalize-space(),'DevOps')]"
    )

    # ── Course cards ───────────────────────────────────────────────────────────
    # Cards are rendered as article or div blocks. Target the outer wrapper.
    COURSE_CARDS = (By.XPATH,
        "//div[.//button[normalize-space()='View Syllabus'] or "
        "      .//button[contains(normalize-space(),'Configure Track')] or "
        "      .//a[normalize-space()='View Syllabus']]"
        "[contains(@class,'rounded') or contains(@class,'card') or contains(@class,'border')]"
    )

    # Fallback: any card that has a 'View Syllabus' child
    COURSE_CARD_ANY = (By.XPATH, "//div[.//a[contains(normalize-space(),'Syllabus')] or .//button[contains(normalize-space(),'Syllabus')]]")

    # Individual card sub-elements (parameterised by card title text)
    def card_title_locator(self, title: str) -> tuple:
        return (By.XPATH, f"//h3[contains(normalize-space(),'{title}')] | //h4[contains(normalize-space(),'{title}')] | //h5[contains(normalize-space(),'{title}')]")

    def card_view_syllabus_locator(self, title: str) -> tuple:
        """Return the 'View Syllabus' button locator within the card for *title*."""
        return (By.XPATH,
            f"//h3[contains(normalize-space(),'{title}')]/ancestor::div[contains(@class,'rounded') or contains(@class,'border')]"
            "//a[contains(normalize-space(),'View Syllabus') or contains(normalize-space(),'Syllabus')]"
            f" | //h4[contains(normalize-space(),'{title}')]/ancestor::div[contains(@class,'rounded') or contains(@class,'border')]"
            "//a[contains(normalize-space(),'View Syllabus')]"
        )

    def card_configure_track_locator(self, title: str) -> tuple:
        """Return the 'Configure Track' button locator within the card for *title*."""
        return (By.XPATH,
            f"//h3[contains(normalize-space(),'{title}')]/ancestor::div[contains(@class,'rounded') or contains(@class,'border')]"
            "//button[contains(normalize-space(),'Configure Track') or contains(normalize-space(),'Configure')]"
            " | "
            f"//h4[contains(normalize-space(),'{title}')]/ancestor::div[contains(@class,'rounded') or contains(@class,'border')]"
            "//button[contains(normalize-space(),'Configure Track')]"
        )

    # Generic "Configure Track" button — first match on page
    CONFIGURE_TRACK_BTN_FIRST = (By.XPATH,
        "//button[contains(normalize-space(),'Configure Track')] | "
        "//a[contains(normalize-space(),'Configure Track')]"
    )

    # Generic "View Syllabus" — first match
    VIEW_SYLLABUS_BTN_FIRST = (By.XPATH,
        "//a[contains(normalize-space(),'View Syllabus')] | "
        "//button[contains(normalize-space(),'View Syllabus')]"
    )

    # Duration element inside any card (e.g. "12 Weeks")
    CARD_DURATION_ELEMENTS = (By.XPATH,
        "//span[contains(normalize-space(),'Week') or contains(normalize-space(),'Hours') or "
        "        contains(normalize-space(),'Month')]"
        "[ancestor::div[.//a[contains(normalize-space(),'Syllabus')]]]"
    )

    # Tech stack tag chips inside cards
    CARD_TECH_TAGS = (By.XPATH,
        "//span[contains(@class,'rounded') and contains(@class,'text-')]"
        "[ancestor::div[.//a[contains(normalize-space(),'Syllabus')]]]"
    )

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Action Methods ─────────────────────────────────────────────────────────

    def load(self, base_url: str) -> None:
        """Navigate to the courses page."""
        url = f"{base_url.rstrip('/')}/courses"
        logger.info("Loading CoursesPage: %s", url)
        self.open(url)

    def get_page_heading(self) -> str:
        return self.wait_and_get_text(self.PAGE_HEADING)

    def click_filter_tab(self, category: str) -> None:
        """
        Click a filter tab by its visible text. Valid values:
            'All Ecosystems', 'Software Engineering', 'Data Science',
            'Infrastructure & DevOps'
        """
        logger.info("Clicking filter tab: '%s'", category)
        locator = (By.XPATH, f"//button[contains(normalize-space(),'{category}')]")
        self.safe_click(locator)

    def get_visible_course_card_count(self) -> int:
        """Return the number of visible course cards currently on the page."""
        cards = self.find_elements(self.COURSE_CARD_ANY)
        visible = [c for c in cards if c.is_displayed()]
        count = len(visible)
        logger.info("Visible course cards: %d", count)
        return count

    def is_course_card_visible(self, title: str) -> bool:
        """Return True if a course card with *title* is visible on the page."""
        loc = self.card_title_locator(title)
        return self.is_element_visible(loc)

    def click_view_syllabus(self, title: str) -> None:
        """Click the 'View Syllabus' link on the card matching *title*."""
        logger.info("Clicking 'View Syllabus' on card: '%s'", title)
        self.safe_click(self.card_view_syllabus_locator(title))

    def click_configure_track(self, title: str) -> None:
        """Click the 'Configure Track' button on the card matching *title*."""
        logger.info("Clicking 'Configure Track' on card: '%s'", title)
        self.safe_click(self.card_configure_track_locator(title))

    def click_first_configure_track(self) -> None:
        """Click the first 'Configure Track' button visible on the page."""
        logger.info("Clicking first available 'Configure Track' button")
        self.safe_click(self.CONFIGURE_TRACK_BTN_FIRST)

    def get_all_filter_tab_texts(self) -> list[str]:
        """Return visible text of all category filter tabs."""
        tabs = self.find_elements(self.ALL_FILTER_TABS)
        return [t.text.strip() for t in tabs if t.text.strip()]

    def are_filter_tabs_present(self) -> bool:
        """Return True if at least one filter tab is visible."""
        return self.is_element_visible(self.FILTER_ALL_ECOSYSTEMS)
