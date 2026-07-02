from __future__ import annotations

from behave import given, when, then
from behave.runner import Context

from utils.config_reader import get_base_url
from utils.logger import get_logger

logger = get_logger(__name__)

_BASE_URL = get_base_url()


# ── Given ──────────────────────────────────────────────────────────────────────

# NOTE: The "I am on the SkillMantra homepage" Given is shared with
# navigation_steps.py. behave resolves step definitions globally, so the
# definition in navigation_steps.py covers this feature too. No duplicate needed.


# ── When ───────────────────────────────────────────────────────────────────────

@when('I click the "Explore Programs" button')
def step_click_explore_programs(context: Context) -> None:
    logger.info("When: clicking 'Explore Programs'")
    context.home_page.click_explore_programs()


@when('I click the "Consult Career Architect" button')
def step_click_consult_career(context: Context) -> None:
    logger.info("When: clicking 'Consult Career Architect'")
    context.home_page.click_consult_career()


@when("I scroll to the contact section")
def step_scroll_to_contact(context: Context) -> None:
    logger.info("When: scrolling to contact / lead form section")
    context.home_page.scroll_to_contact_section()


# ── Then ───────────────────────────────────────────────────────────────────────

@then("the hero headline should be visible")
def step_hero_headline_visible(context: Context) -> None:
    visible = context.home_page.is_hero_headline_visible()
    assert visible, "Hero headline is NOT visible on the homepage."


@then('the hero headline should contain "{expected_text}"')
def step_hero_headline_text(context: Context, expected_text: str) -> None:
    actual = context.home_page.get_hero_headline_text()
    logger.info("Hero headline text: '%s'", actual)
    assert expected_text.lower() in actual.lower(), (
        f"Hero headline '{actual}' does not contain '{expected_text}'"
    )


@then('the "Explore Programs" CTA button should be visible')
def step_explore_programs_visible(context: Context) -> None:
    visible = context.home_page.is_explore_programs_btn_visible()
    assert visible, "'Explore Programs' CTA button is NOT visible."


@then('the "Consult Career Architect" CTA button should be visible')
def step_consult_career_visible(context: Context) -> None:
    visible = context.home_page.is_consult_career_btn_visible()
    assert visible, "'Consult Career Architect' CTA button is NOT visible."


@then('the stats section should show "{expected_value}" global rating')
def step_stats_rating(context: Context, expected_value: str) -> None:
    actual = context.home_page.get_stat_rating_text()
    logger.info("Rating stat text: '%s'", actual)
    # The site renders '4.8\u2605' (4.8 + Unicode star). expected_value may be '4.8*' (ASCII).
    # We strip non-alphanumeric suffixes and compare the numeric part.
    expected_base = expected_value.rstrip('*').rstrip('\u2605').strip()
    assert expected_base in actual, (
        f"Stats section rating text '{actual}' does not contain '{expected_base}'"
    )


@then('the stats section should show "{expected_value}" for Live Labs')
def step_stats_live_labs(context: Context, expected_value: str) -> None:
    actual = context.home_page.get_stat_live_labs_text()
    logger.info("Live Labs stat text: '%s'", actual)
    assert expected_value in actual, (
        f"Stats 'Live Labs' value '{actual}' does not contain '{expected_value}'"
    )


@then('the stats section should show "{expected_value}" for Doubt Sync')
def step_stats_doubt_sync(context: Context, expected_value: str) -> None:
    actual = context.home_page.get_stat_doubt_sync_text()
    logger.info("Doubt Sync stat text: '%s'", actual)
    assert expected_value in actual, (
        f"Stats 'Doubt Sync' value '{actual}' does not contain '{expected_value}'"
    )


@then('the course card for "{course_name}" should be visible')
def step_course_card_visible(context: Context, course_name: str) -> None:
    from selenium.webdriver.common.by import By
    locator = (By.XPATH, f"//h5[contains(normalize-space(),'{course_name}')]")
    visible = context.home_page.is_element_visible(locator)
    assert visible, f"Course preview card for '{course_name}' is NOT visible on the homepage."


@then("at least 3 course preview cards should be visible in the hero panel")
def step_three_hero_cards_visible(context: Context) -> None:
    count = context.home_page.count_hero_course_cards()
    logger.info("Hero panel course card count: %d", count)
    assert count >= 3, (
        f"Expected at least 3 hero course preview cards, but found {count}."
    )


@then('the page URL should contain "#courses" or the courses section should be in view')
def step_explore_programs_destination(context: Context) -> None:
    """
    After clicking 'Explore Programs', the page either scrolls to #courses (anchor)
    or navigates to /courses. We check for either.
    """
    current_url = context.home_page.get_current_url()
    logger.info("URL after 'Explore Programs' click: %s", current_url)
    url_ok = "#courses" in current_url or "/courses" in current_url
    # Also check if the courses section is scrolled into view
    section_visible = context.home_page.is_element_visible(
        context.home_page.COURSES_SECTION, timeout=5
    )
    assert url_ok or section_visible, (
        f"After clicking 'Explore Programs', URL='{current_url}' and courses section "
        f"visible={section_visible}. Expected '#courses' in URL or section to be visible."
    )


@then('the URL should contain "#contact" or the contact section should be in view')
def step_consult_career_destination(context: Context) -> None:
    """
    After clicking 'Consult Career Architect', the page scrolls to #contact.
    """
    current_url = context.home_page.get_current_url()
    logger.info("URL after 'Consult Career Architect' click: %s", current_url)
    url_ok = "#contact" in current_url
    section_visible = context.home_page.is_element_visible(
        context.home_page.LEAD_FORM_SECTION, timeout=5
    )
    assert url_ok or section_visible, (
        f"After clicking 'Consult Career Architect', URL='{current_url}' and "
        f"contact section visible={section_visible}."
    )


@then("the lead form section should be present on the page")
def step_lead_form_present(context: Context) -> None:
    present = context.home_page.is_element_present(
        context.home_page.LEAD_FORM_SECTION, timeout=10
    )
    assert present, "Lead form section (#contact) is NOT present on the homepage."


@then("the Full Stack program option should be visible in the lead form")
def step_lead_form_fullstack_visible(context: Context) -> None:
    present = context.home_page.is_element_present(
        context.home_page.LEAD_FORM_CHECKBOX_FULLSTACK, timeout=8
    )
    assert present, "Full Stack program checkbox/option is NOT present in the lead form."


@then("the ML Engineer program option should be visible in the lead form")
def step_lead_form_ml_visible(context: Context) -> None:
    present = context.home_page.is_element_present(
        context.home_page.LEAD_FORM_CHECKBOX_ML, timeout=8
    )
    assert present, "ML Engineer program checkbox/option is NOT present in the lead form."


@then("the QA Testing Automation Track option should be visible in the lead form")
def step_lead_form_qa_visible(context: Context) -> None:
    present = context.home_page.is_element_present(
        context.home_page.LEAD_FORM_CHECKBOX_QA, timeout=8
    )
    assert present, "QA Testing Automation Track option is NOT present in the lead form."


@then("the lead form submit button should be visible")
def step_lead_form_submit_visible(context: Context) -> None:
    visible = context.home_page.is_element_visible(
        context.home_page.LEAD_FORM_SUBMIT_BTN, timeout=8
    )
    assert visible, "Lead form submit button is NOT visible."
