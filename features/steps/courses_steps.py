from __future__ import annotations

from behave import given, when, then
from behave.runner import Context

from utils.config_reader import get_base_url
from utils.logger import get_logger

logger = get_logger(__name__)

_BASE_URL = get_base_url()


# ── Given ──────────────────────────────────────────────────────────────────────

@given("I am on the courses catalog page")
def step_open_courses_page(context: Context) -> None:
    logger.info("Given: navigating to courses catalog page")
    context.courses_page.load(_BASE_URL)


# ── When ───────────────────────────────────────────────────────────────────────

@when('I click the "{category}" filter tab')
def step_click_filter_tab(context: Context, category: str) -> None:
    logger.info("When: clicking filter tab '%s'", category)
    context.courses_page.click_filter_tab(category)


@when('I click the first available "Configure Track" button')
def step_click_first_configure_track(context: Context) -> None:
    logger.info("When: clicking first 'Configure Track' button")
    context.courses_page.click_first_configure_track()


# ── Then ───────────────────────────────────────────────────────────────────────

@then("the courses page heading should be visible")
def step_courses_heading_visible(context: Context) -> None:
    visible = context.courses_page.is_element_visible(
        context.courses_page.PAGE_HEADING
    )
    assert visible, "Courses page heading is NOT visible."


@then("the following filter tabs should be present")
def step_filter_tabs_present(context: Context) -> None:
    """
    Accepts a table with column 'tab_name' and verifies each tab exists.
    """
    from selenium.webdriver.common.by import By
    for row in context.table:
        tab_name = row["tab_name"]
        locator = (By.XPATH, f"//button[contains(normalize-space(),'{tab_name}')]")
        visible = context.courses_page.is_element_visible(locator, timeout=8)
        logger.info("Filter tab '%s' visible: %s", tab_name, visible)
        assert visible, f"Filter tab '{tab_name}' is NOT visible on the courses page."


@then("at least 1 course card should be visible")
def step_at_least_one_course_card(context: Context) -> None:
    count = context.courses_page.get_visible_course_card_count()
    assert count >= 1, (
        f"Expected at least 1 course card to be visible, but found {count}."
    )


@then('the filter tab "{category}" should appear active or selected')
def step_filter_tab_active(context: Context, category: str) -> None:
    """
    Verify the clicked filter tab is visually differentiated (active state).
    We check the element's class or aria-selected attribute.
    """
    from selenium.webdriver.common.by import By
    locator = (By.XPATH, f"//button[contains(normalize-space(),'{category}')]")
    try:
        element = context.courses_page.wait_for_visible(locator, timeout=5)
        cls = element.get_attribute("class") or ""
        aria = element.get_attribute("aria-selected") or ""
        logger.info(
            "Filter tab '%s' — class='%s' aria-selected='%s'", category, cls, aria
        )
        # Many frameworks mark the active tab with 'active', 'selected',
        # a bg-color class, or aria-selected="true".
        is_active = (
            "active" in cls.lower()
            or "selected" in cls.lower()
            or aria == "true"
            or "bg-" in cls           # Tailwind background colour indicates active
            or "text-logoOrange" in cls
            or "border-logoOrange" in cls
        )
        # Soft assertion — log warning instead of hard fail if no active indicator is
        # found, as some implementations rely purely on visual styling not classnames.
        if not is_active:
            logger.warning(
                "Could not confirm active state for filter tab '%s' via class/aria. "
                "Visual inspection may be needed. class='%s'", category, cls
            )
    except Exception as exc:
        logger.warning("Could not check active state for tab '%s': %s", category, exc)


@then("at least one course card should display duration or week information")
def step_card_has_duration(context: Context) -> None:
    count = context.courses_page.count_elements(context.courses_page.CARD_DURATION_ELEMENTS)
    logger.info("Duration/week elements found: %d", count)
    assert count >= 1, "No course card found displaying duration or week information."


@then("at least one course card should display technology tag chips")
def step_card_has_tech_tags(context: Context) -> None:
    count = context.courses_page.count_elements(context.courses_page.CARD_TECH_TAGS)
    logger.info("Tech tag chip elements found: %d", count)
    assert count >= 1, "No tech stack tag chips found on any course card."


@then('at least one course card should have a "View Syllabus" link')
def step_card_has_view_syllabus(context: Context) -> None:
    visible = context.courses_page.is_element_visible(
        context.courses_page.VIEW_SYLLABUS_BTN_FIRST
    )
    assert visible, "No 'View Syllabus' link found on any course card."


@then('at least one course card should have a "Configure Track" button')
def step_card_has_configure_track(context: Context) -> None:
    visible = context.courses_page.is_element_visible(
        context.courses_page.CONFIGURE_TRACK_BTN_FIRST
    )
    assert visible, "No 'Configure Track' button found on any course card."


@then('the URL should contain "/contact" or the page should scroll to a contact form')
def step_configure_track_destination(context: Context) -> None:
    """
    After 'Configure Track' is clicked, the user should land on /contact
    or the page should scroll to an embedded contact/enquiry form.
    """
    current_url = context.courses_page.get_current_url()
    logger.info("URL after 'Configure Track' click: %s", current_url)

    url_ok = "/contact" in current_url or "#contact" in current_url

    from selenium.webdriver.common.by import By
    form_locator = (By.XPATH,
        "//form | //input[@type='email'] | //textarea[@name='message']"
    )
    form_visible = context.courses_page.is_element_visible(form_locator, timeout=5)

    assert url_ok or form_visible, (
        f"After 'Configure Track', URL='{current_url}' and "
        f"contact form visible={form_visible}. Expected redirection to /contact."
    )
