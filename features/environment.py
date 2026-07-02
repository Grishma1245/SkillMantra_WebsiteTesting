"""
environment.py
--------------
behave lifecycle hooks for the SkillMantra automation framework.

Hook execution order:
  before_all → before_feature → before_scenario → [steps] → after_scenario → after_feature → after_all

Key responsibilities:
  - Initialise WebDriver via DriverFactory before each scenario
  - Attach page objects to context so step defs can access them
  - Capture screenshot on step failure and embed in HTML/Allure report
  - Quit WebDriver cleanly after every scenario (even on failure)
  - Configure logging for the session
"""

from __future__ import annotations

import base64
import logging
import os
from datetime import datetime

from behave.model import Scenario, Step, Feature
from behave.runner import Context

from utils.config_reader import get_base_url, is_screenshot_on_failure
from utils.driver_factory import get_driver
from utils.logger import get_logger

logger = get_logger("environment")

# Screenshot output directory
_SCREENSHOT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "reports", "screenshots"
)
os.makedirs(_SCREENSHOT_DIR, exist_ok=True)


# ── Session-level hooks ────────────────────────────────────────────────────────

def before_all(context: Context) -> None:
    """
    Runs once before the entire test suite.
    Stores shared config on the context object.
    """
    logger.info("=" * 70)
    logger.info("  SkillMantra Automation Suite — starting")
    logger.info("  Base URL   : %s", get_base_url())
    logger.info("  Timestamp  : %s", datetime.now().isoformat(timespec="seconds"))
    logger.info("=" * 70)

    context.base_url = get_base_url()
    context.take_screenshot_on_failure = is_screenshot_on_failure()

    # Attach behave HTML formatter config if available
    context.config.setup_logging(logging.INFO)


def after_all(context: Context) -> None:
    """Runs once after the entire test suite."""
    logger.info("=" * 70)
    logger.info("  SkillMantra Automation Suite — finished")
    logger.info("=" * 70)


# ── Feature-level hooks ────────────────────────────────────────────────────────

def before_feature(context: Context, feature: Feature) -> None:
    logger.info("▶ FEATURE: %s", feature.name)


def after_feature(context: Context, feature: Feature) -> None:
    logger.info("◀ FEATURE done: %s", feature.name)


# ── Scenario-level hooks ───────────────────────────────────────────────────────

def before_scenario(context: Context, scenario: Scenario) -> None:
    """
    Launch a fresh WebDriver instance before each scenario and attach
    all Page Object instances to the context.
    """
    logger.info("  ↳ SCENARIO start: %s", scenario.name)

    # Initialise driver
    context.driver = get_driver()

    # Lazy-import page objects here to avoid circular imports at module load
    from pages.home_page import HomePage
    from pages.courses_page import CoursesPage
    from pages.contact_page import ContactPage

    context.home_page    = HomePage(context.driver)
    context.courses_page = CoursesPage(context.driver)
    context.contact_page = ContactPage(context.driver)


def after_scenario(context: Context, scenario: Scenario) -> None:
    """
    After each scenario:
      1. If the scenario FAILED and screenshots are enabled, capture one.
      2. Quit the WebDriver — guaranteed even if step raised an exception.
    """
    if scenario.status == "failed":
        logger.warning("  ✗ SCENARIO failed: %s", scenario.name)

        if getattr(context, "take_screenshot_on_failure", True):
            _capture_screenshot(context, scenario)
    else:
        logger.info("  ✔ SCENARIO passed: %s", scenario.name)

    # Always quit the driver (no resource leaks)
    driver = getattr(context, "driver", None)
    if driver is not None:
        try:
            driver.quit()
            logger.debug("  WebDriver quit cleanly.")
        except Exception as exc:
            logger.warning("  WebDriver quit raised an exception: %s", exc)
    context.driver = None


# ── Step-level hooks ───────────────────────────────────────────────────────────

def before_step(context: Context, step: Step) -> None:
    logger.debug("    STEP: %s %s", step.step_type.upper(), step.name)


def after_step(context: Context, step: Step) -> None:
    if step.status == "failed":
        logger.error("    STEP FAILED: %s %s", step.step_type.upper(), step.name)
        if step.error_message:
            logger.error("    Error: %s", step.error_message[:500])


# ── Private helpers ────────────────────────────────────────────────────────────

def _capture_screenshot(context: Context, scenario: Scenario) -> None:
    """Take a screenshot and attach it to the behave report."""
    driver = getattr(context, "driver", None)
    if driver is None:
        logger.warning("Cannot take screenshot — driver is None.")
        return

    # Sanitize scenario name to avoid illegal filesystem characters like double quotes on Windows
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    clean_name = scenario.name
    for char in illegal_chars:
        clean_name = clean_name.replace(char, '')
    safe_name = clean_name.replace(" ", "_")[:80]
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename   = f"{safe_name}__{timestamp}.png"
    filepath   = os.path.join(_SCREENSHOT_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        logger.info("  Screenshot saved: %s", filepath)

        # Embed into behave HTML / Allure report
        with open(filepath, "rb") as f:
            png_bytes = f.read()

        # behave-html-formatter: attach as MIME data (only available when HTML formatter is active)
        try:
            context.embed("image/png", base64.b64encode(png_bytes).decode("utf-8"), caption=f"Failure: {scenario.name}")
        except AttributeError:
            # Running with 'pretty' or other formatter — embed not available, screenshot already saved to disk
            logger.debug("  context.embed not available (not running with HTML formatter). Screenshot saved to disk only.")

    except Exception as exc:
        logger.warning("  Failed to save screenshot: %s", exc)
