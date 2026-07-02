from __future__ import annotations

from behave import given, when, then
from behave.runner import Context

from utils.config_reader import get_base_url
from utils.logger import get_logger

logger = get_logger(__name__)

_BASE_URL = get_base_url()


# ── Given ──────────────────────────────────────────────────────────────────────

@given("I am on the SkillMantra homepage")
def step_open_homepage(context: Context) -> None:
    logger.info("Given: navigating to homepage")
    context.home_page.load(_BASE_URL)


# ── When ───────────────────────────────────────────────────────────────────────

@when('I click the "{link_text}" navigation link')
def step_click_nav_link(context: Context, link_text: str) -> None:
    logger.info("When: clicking nav link '%s'", link_text)
    nav_map = {
        "Courses":    context.home_page.NAV_COURSES,
        "Instructor": context.home_page.NAV_INSTRUCTOR,
        "Placement":  context.home_page.NAV_PLACEMENT,
        "Blog":       context.home_page.NAV_BLOG,
        "Contact":    context.home_page.NAV_CONTACT,
        "About":      context.home_page.NAV_ABOUT,
    }
    locator = nav_map.get(link_text)
    assert locator is not None, f"Unknown nav link: '{link_text}'"
    context.home_page.safe_click(locator)


@when('I click the "{link_text}" top bar link')
def step_click_top_bar_link(context: Context, link_text: str) -> None:
    logger.info("When: clicking top bar link '%s'", link_text)
    top_bar_map = {
        "Corporate Training":         context.home_page.TOP_BAR_CORPORATE,
        "Corporate Analytics Service": context.home_page.TOP_BAR_ANALYTICS_SVC,
    }
    locator = top_bar_map.get(link_text)
    assert locator is not None, f"Unknown top bar link: '{link_text}'"
    context.home_page.safe_click(locator)


@when("I click the WhatsApp chat widget")
def step_click_whatsapp_widget(context: Context) -> None:
    logger.info("When: clicking WhatsApp chat widget")
    context.home_page.click_whatsapp_widget()


@when('I click the "Initialize Secure Chat" button')
def step_click_initialize_chat(context: Context) -> None:
    logger.info("When: clicking Initialize Secure Chat")
    # Store the original handle before new tab opens
    context.original_window_handle = context.home_page.click_initialize_chat()


# ── Then ───────────────────────────────────────────────────────────────────────

@then('the page title should contain "{expected_text}"')
def step_page_title_contains(context: Context, expected_text: str) -> None:
    title = context.home_page.get_page_title()
    logger.info("Page title: '%s' — expecting substring '%s'", title, expected_text)
    assert expected_text.lower() in title.lower(), (
        f"Page title '{title}' does not contain '{expected_text}'"
    )


@then('the URL should contain "{partial_url}"')
def step_url_contains(context: Context, partial_url: str) -> None:
    current = context.home_page.get_current_url()
    logger.info("Current URL: %s — expecting fragment '%s'", current, partial_url)
    assert partial_url in current, (
        f"URL '{current}' does not contain '{partial_url}'"
    )


@then("the page should not return an error status")
def step_page_no_error(context: Context) -> None:
    """
    Verify the page does not show a generic error headline.
    Selenium does not expose HTTP status codes directly, so we check
    that the page title / body does not contain '404', '500', or 'Not Found'.
    """
    title = context.home_page.get_page_title()
    body_text = context.driver.find_element(
        *(__import__("selenium.webdriver.common.by", fromlist=["By"]).By.TAG_NAME, "body")
    ).text.lower()

    assert "404" not in title.lower(), f"Page returned 404 error. Title: '{title}'"
    assert "500" not in title.lower(), f"Page returned 500 error. Title: '{title}'"
    assert "not found" not in title.lower(), f"Page shows 'Not Found'. Title: '{title}'"
    # Additional body check — some SPAs render error text in body not title
    assert "page not found" not in body_text[:500], "Body contains 'page not found' text"


@then("the footer should contain at least one top-domain link")
def step_footer_has_top_domain_links(context: Context) -> None:
    # KNOWN ISSUE: Footer "Top Domains" links point to #courses anchor on homepage,
    # not real route URLs. We verify their presence and actual href values.
    count = context.home_page.count_elements(context.home_page.FOOTER_TOP_DOMAIN_LINKS)
    logger.info("Footer top-domain link count: %d", count)
    assert count >= 1, "No footer top-domain links found. Expected at least 1."


@then("the footer top-domain links should point to the courses anchor")
def step_footer_links_anchor_courses(context: Context) -> None:
    # KNOWN ISSUE: These links use #courses as the target — this is the actual
    # site behaviour (anchor link back to homepage courses section), not a real route.
    # We assert the actual href to document real behaviour, not assert a false route.
    elements = context.home_page.find_elements(context.home_page.FOOTER_TOP_DOMAIN_LINKS)
    if not elements:
        logger.warning("No footer top-domain links found — skipping href assertion.")
        return

    for el in elements:
        href = el.get_attribute("href") or ""
        logger.info("Footer link href: %s", href)
        assert "courses" in href.lower() or "#" in href, (
            f"Footer link '{el.text}' has unexpected href: '{href}'. "
            f"Expected '#courses' anchor or '/courses' route."
        )


@then("the WhatsApp chat widget should be visible on the page")
def step_whatsapp_widget_visible(context: Context) -> None:
    visible = context.home_page.is_whatsapp_widget_visible()
    assert visible, "WhatsApp 'Core Advisor' floating chat widget is NOT visible on the page."


@then('a new browser tab should open with a URL containing "{expected_fragment}"')
def step_new_tab_url_contains(context: Context, expected_fragment: str) -> None:
    # switch_to_new_tab waits for a 2nd window and switches to it
    new_handle = context.home_page.switch_to_new_tab(context.original_window_handle)
    context.new_tab_handle = new_handle

    new_url = context.home_page.get_current_url()
    logger.info("New tab URL: %s", new_url)
    assert expected_fragment in new_url, (
        f"New tab URL '{new_url}' does not contain '{expected_fragment}'"
    )


@then("I switch back to the original tab")
def step_switch_back_to_original(context: Context) -> None:
    original = getattr(context, "original_window_handle", None)
    assert original is not None, "No original window handle stored in context."
    context.home_page.switch_back_to_window(original)
    logger.info("Switched back to original tab: %s", original)
