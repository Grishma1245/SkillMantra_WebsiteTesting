from __future__ import annotations

from behave import given, when, then
from behave.runner import Context
from selenium.common.exceptions import UnexpectedAlertPresentException

from utils.config_reader import get_base_url
from utils.logger import get_logger

logger = get_logger(__name__)

_BASE_URL = get_base_url()


# ── Given ──────────────────────────────────────────────────────────────────────

@given("I am on the contact page")
def step_open_contact_page(context: Context) -> None:
    logger.info("Given: navigating to contact page")
    context.contact_page.load(_BASE_URL)


# ── When ───────────────────────────────────────────────────────────────────────

@when("I fill in the contact form with")
def step_fill_contact_form_table(context: Context) -> None:
    """
    Fills contact form fields from a Gherkin table with columns: field | value.

    Example:
        | field   | value            |
        | name    | John Doe         |
        | email   | john@example.com |
    """
    if context.table is None:
        raise ValueError("Step requires a data table (| field | value |)")

    for row in context.table:
        field = row["field"].strip().lower()
        value = row["value"].strip()
        logger.info("Filling field '%s' = '%s'", field, value)
        context.contact_page.fill_field(field, value)


@when("I submit the contact form")
def step_submit_contact_form(context: Context) -> None:
    logger.info("When: submitting the contact form")
    context.contact_page.submit_form()


@when('I submit the contact form without filling in "{field}"')
def step_submit_form_missing_field(context: Context, field: str) -> None:
    """
    Fill all required fields EXCEPT the specified one, then submit.
    Used in the 'empty required fields' Scenario Outline.
    """
    logger.info("When: submitting form leaving '%s' empty", field)

    all_fields = {
        "name":    ("Test User",           context.contact_page.FORM_FULL_NAME),
        "phone":   ("+977 9800000001",     context.contact_page.FORM_PHONE),
        "email":   ("valid@testmail.com",  context.contact_page.FORM_EMAIL),
        "subject": ("Test Subject",        context.contact_page.FORM_SUBJECT),
        "message": ("Test message body.",  context.contact_page.FORM_MESSAGE),
    }

    for fname, (fvalue, flocator) in all_fields.items():
        if fname == field.strip().lower():
            logger.debug("Skipping field '%s' (intentionally left empty)", fname)
            continue
        try:
            context.contact_page.safe_send_keys(flocator, fvalue, timeout=5)
        except Exception as exc:
            logger.warning("Could not fill field '%s': %s", fname, exc)

    context.contact_page.submit_form()


# ── Then ───────────────────────────────────────────────────────────────────────

@then("the success confirmation message should appear")
def step_success_message_visible(context: Context) -> None:
    visible = context.contact_page.is_success_message_visible(timeout=20)
    assert visible, (
        "Success confirmation message ('Transmission Successful') did NOT appear "
        "after submitting the contact form."
    )
    logger.info("Success message text: '%s'", context.contact_page.get_success_message_text())


@then('the form should indicate "{field}" is required')
def step_form_field_required_error(context: Context, field: str) -> None:
    """
    After attempting to submit with an empty required field, verify either:
      a) HTML5 native validation marks the field as invalid, or
      b) A custom validation error message is visible.
    """
    field_map = {
        "name":    context.contact_page.FORM_FULL_NAME,
        "phone":   context.contact_page.FORM_PHONE,
        "email":   context.contact_page.FORM_EMAIL,
        "subject": context.contact_page.FORM_SUBJECT,
        "message": context.contact_page.FORM_MESSAGE,
    }

    locator = field_map.get(field.strip().lower())
    assert locator is not None, f"Unknown field name: '{field}'"

    # Check HTML5 native validation (works for required fields)
    is_invalid = context.contact_page.is_field_invalid(locator)
    native_msg = context.contact_page.get_html5_validation_message(locator)
    custom_errors_visible = context.contact_page.are_validation_errors_visible(timeout=4)

    logger.info(
        "Validation for empty '%s': is_invalid=%s | native_msg='%s' | custom_errors=%s",
        field, is_invalid, native_msg, custom_errors_visible,
    )

    assert is_invalid or custom_errors_visible or native_msg, (
        f"Field '{field}' should be marked as required/invalid after empty submission, "
        f"but no validation error was detected. "
        f"HTML5 invalid={is_invalid}, native_msg='{native_msg}', "
        f"custom_errors_visible={custom_errors_visible}."
    )


@then("the form should show an email validation error")
def step_form_email_validation_error(context: Context) -> None:
    """
    After submitting with an invalid email, verify the email field is invalid.
    Checks HTML5 type="email" validation or a custom error message.
    """
    is_invalid = context.contact_page.is_field_invalid(context.contact_page.FORM_EMAIL)
    native_msg = context.contact_page.get_html5_validation_message(context.contact_page.FORM_EMAIL)
    custom_errors = context.contact_page.are_validation_errors_visible(timeout=4)

    logger.info(
        "Email validation: is_invalid=%s | native_msg='%s' | custom_errors=%s",
        is_invalid, native_msg, custom_errors,
    )

    assert is_invalid or custom_errors or native_msg, (
        "Expected an email validation error after submitting an invalid email address, "
        f"but none was detected. HTML5 invalid={is_invalid}, native_msg='{native_msg}'."
    )


@then("the form should show a phone validation error or reject the submission")
def step_form_phone_validation_error(context: Context) -> None:
    """
    After submitting with an invalid phone, verify either:
      - The field is marked as invalid (HTML5), or
      - A custom error is displayed, or
      - The success message does NOT appear (form rejected the submission).
    """
    is_invalid = context.contact_page.is_field_invalid(context.contact_page.FORM_PHONE)
    native_msg = context.contact_page.get_html5_validation_message(context.contact_page.FORM_PHONE)
    custom_errors = context.contact_page.are_validation_errors_visible(timeout=4)
    success_shown = context.contact_page.is_success_message_visible(timeout=3)

    logger.info(
        "Phone validation: is_invalid=%s | native_msg='%s' | custom_errors=%s | success=%s",
        is_invalid, native_msg, custom_errors, success_shown,
    )

    assert (is_invalid or custom_errors or native_msg) or not success_shown, (
        "Phone validation: expected the form to either show a validation error or "
        "NOT show the success message. Form appeared to accept an invalid phone number."
    )


@then("the page should not crash or display a server error")
def step_no_crash_or_server_error(context: Context) -> None:
    """
    After boundary input, verify no server-side error is rendered.
    """
    title = context.driver.title.lower()
    body_text = context.driver.find_element(
        *(__import__("selenium.webdriver.common.by", fromlist=["By"]).By.TAG_NAME, "body")
    ).text.lower()

    assert "500" not in title, f"Page shows 500 Internal Server Error. Title: '{title}'"
    assert "error" not in title or "skillmantra" in title, (
        f"Unexpected error in page title: '{title}'"
    )
    assert "internal server error" not in body_text[:1000], (
        "Page body contains 'internal server error' text."
    )
    logger.info("No crash or server error detected after boundary input submission.")


@then("no JavaScript alert dialog should appear")
def step_no_js_alert(context: Context) -> None:
    """
    Verify the injected XSS payload did not trigger a JavaScript alert().
    Selenium raises UnexpectedAlertPresentException if an alert is open.
    We proactively check by attempting to switch to an alert.
    """
    try:
        alert = context.driver.switch_to.alert
        alert_text = alert.text
        alert.dismiss()
        raise AssertionError(
            f"SECURITY ISSUE: A JavaScript alert was triggered by XSS input! "
            f"Alert text: '{alert_text}'"
        )
    except Exception as exc:
        if "AssertionError" in type(exc).__name__ or "SECURITY ISSUE" in str(exc):
            raise
        # NoAlertPresentException — this is expected (good)
        logger.info("No JavaScript alert present — XSS alert was not triggered.")


@then("the page should not execute the injected script")
def step_xss_not_executed(context: Context) -> None:
    """
    Secondary XSS check: verify the raw script tag is not present in the rendered DOM
    as an actual executable element (it should be escaped or stripped).
    """
    from selenium.webdriver.common.by import By
    # Look for an actual <script> element in the DOM that was injected
    injected_scripts = context.driver.find_elements(
        By.XPATH,
        "//script[contains(text(),\"alert('XSS-1')\")]"
    )
    if injected_scripts:
        raise AssertionError(
            "SECURITY ISSUE: Injected <script> element found live in the DOM! "
            "The XSS payload was NOT sanitised."
        )
    logger.info("XSS check passed — no injected <script> element found in DOM.")


@then('the contact page should display phone number "{expected_phone}"')
def step_contact_phone_displayed(context: Context, expected_phone: str) -> None:
    actual = context.contact_page.get_contact_phone_text()
    logger.info("Contact phone text: '%s' | expected: '%s'", actual, expected_phone)
    assert expected_phone in actual, (
        f"Expected phone '{expected_phone}' not found. Actual: '{actual}'"
    )


@then('the contact page should display email "{expected_email}"')
def step_contact_email_displayed(context: Context, expected_email: str) -> None:
    actual = context.contact_page.get_contact_email_text()
    logger.info("Contact email text: '%s' | expected: '%s'", actual, expected_email)
    assert expected_email in actual, (
        f"Expected email '{expected_email}' not found. Actual: '{actual}'"
    )


@then("the Google Maps iframe should be present on the page")
def step_maps_iframe_present(context: Context) -> None:
    present = context.contact_page.is_maps_iframe_present()
    assert present, "Google Maps embed iframe is NOT present on the contact page."
