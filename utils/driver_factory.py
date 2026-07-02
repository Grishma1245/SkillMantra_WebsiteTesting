"""
driver_factory.py
-----------------
Creates and returns a configured Selenium WebDriver instance.

Supported browsers  : chrome | firefox | edge
Headless toggle     : set HEADLESS=true in environment or config.ini
Driver management   : webdriver-manager (auto-downloads matching driver binary)
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.config_reader import get_browser, get_timeout, is_headless
from utils.logger import get_logger

logger = get_logger(__name__)


def get_driver() -> webdriver.Remote:
    """
    Instantiate and return a WebDriver based on current config.

    Returns:
        A configured selenium.webdriver instance.

    Raises:
        ValueError: If an unsupported browser name is specified.
    """
    browser = get_browser()
    headless = is_headless()
    timeout = get_timeout()

    logger.info("Initialising browser: %s | headless: %s | timeout: %ss", browser, headless, timeout)

    driver: webdriver.Remote

    if browser == "chrome":
        driver = _build_chrome(headless)
    elif browser == "firefox":
        driver = _build_firefox(headless)
    elif browser == "edge":
        driver = _build_edge(headless)
    else:
        raise ValueError(
            f"Unsupported browser '{browser}'. Valid options: chrome, firefox, edge."
        )

    driver.implicitly_wait(0)            # Use explicit waits only (per design requirement)
    driver.set_page_load_timeout(timeout + 10)
    driver.maximize_window()

    logger.info("WebDriver initialised successfully for '%s'", browser)
    return driver


# ── Private builder helpers ────────────────────────────────────────────────────

def _build_chrome(headless: bool) -> webdriver.Chrome:
    opts = ChromeOptions()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--log-level=3")
    # Suppress 'Chrome is being controlled by automated software' banner
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    if headless:
        opts.add_argument("--headless=new")   # Chromium new headless mode
        logger.debug("Chrome started in headless mode")

    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def _build_firefox(headless: bool) -> webdriver.Firefox:
    opts = FirefoxOptions()
    opts.set_preference("dom.webnotifications.enabled", False)
    opts.set_preference("media.volume_scale", "0.0")

    if headless:
        opts.add_argument("--headless")
        logger.debug("Firefox started in headless mode")

    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=opts)


def _build_edge(headless: bool) -> webdriver.Edge:
    opts = EdgeOptions()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

    if headless:
        opts.add_argument("--headless=new")
        logger.debug("Edge started in headless mode")

    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=opts)
