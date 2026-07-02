"""
contact_page.py
---------------
Page Object for the SkillMantra Contact page (https://skillmantraedu.com/contact).

Locators are derived from the live DOM. The contact form uses standard HTML5 inputs
with Tailwind styling. There are no auto-generated IDs, so we target by `name`,
`placeholder`, and structural XPaths.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.config_reader import get_timeout
from utils.logger import get_logger

logger = get_logger(__name__)


class ContactPage(BasePage):
    """Page Object for the Contact / Enquiry page."""

    # ── Page heading ───────────────────────────────────────────────────────────
    PAGE_HEADING   = (By.CSS_SELECTOR, "section h1")
    PAGE_SUB_LABEL = (By.XPATH, "//*[contains(normalize-space(),'Communication Grid') or contains(normalize-space(),'Synchronize')]")

    # ── Contact form inputs ───────────────────────────────────────────────
    # Locators derived from live DOM inspection:
    #   form id="enquirySystem"
    #   Full Name   : id="usr_name"     name="full_name"      placeholder="John Doe"
    #   Phone       : id="usr_phone"    name="phone_number"   placeholder="+977 98..."
    #   Email       : id="usr_email"    name="email_address"  placeholder="operator@domain.com"
    #   Subject     : id="target_track" name="subject"        placeholder="E.g., Curriculum..."
    #   Message     : id="usr_msg"      name="message"
    FORM_FULL_NAME = (By.CSS_SELECTOR, "#usr_name")
    FORM_PHONE     = (By.CSS_SELECTOR, "#usr_phone")
    FORM_EMAIL     = (By.CSS_SELECTOR, "#usr_email")
    FORM_SUBJECT   = (By.CSS_SELECTOR, "#target_track")
    FORM_MESSAGE   = (By.CSS_SELECTOR, "#usr_msg")
    FORM_SUBMIT_BTN = (By.CSS_SELECTOR, "#enquirySystem button[type='submit']")

    # ── Form validation messages ───────────────────────────────────────────
    # Live DOM: each field has a sibling <p id="error_<field_name>"> with class
    # 'text-rose-500' that is toggled via 'hidden' class by JS validation.
    # Example: <p class="text-rose-500 ... hidden" id="error_full_name"></p>
    VALIDATION_MSG_ANY = (By.XPATH,
        "//p[starts-with(@id,'error_') and not(contains(@class,'hidden')) and normalize-space()]"
        " | //p[contains(@class,'text-rose') and not(contains(@class,'hidden')) and normalize-space()]"
    )
    # Individual field error elements
    ERROR_FULL_NAME    = (By.CSS_SELECTOR, "#error_full_name")
    ERROR_PHONE        = (By.CSS_SELECTOR, "#error_phone_number")
    ERROR_EMAIL        = (By.CSS_SELECTOR, "#error_email_address")
    ERROR_SUBJECT      = (By.CSS_SELECTOR, "#error_subject")
    ERROR_MESSAGE      = (By.CSS_SELECTOR, "#error_message")

    # ── Success message ────────────────────────────────────────────────────
    # Live DOM: success is shown in a div/section revealed after AJAX submit.
    # The text 'Transmission Successful' is used by the site.
    FORM_SUCCESS_MSG = (By.XPATH,
        "//*[contains(normalize-space(),'Transmission Successful') or "
        "    contains(normalize-space(),'Transmission') or "
        "    contains(normalize-space(),'Successfully') or "
        "    contains(normalize-space(),'Thank you') or "
        "    contains(normalize-space(),'Message Sent') or "
        "    contains(normalize-space(),'Sent Successfully')]"
        "[not(ancestor::form)]"
    )

    # ── Contact detail elements ────────────────────────────────────────────────
    CONTACT_PHONE_TEXT  = (By.XPATH, "//*[contains(normalize-space(),'+977 9843095969')]")
    CONTACT_EMAIL_TEXT  = (By.XPATH, "//*[contains(normalize-space(),'info@skillmantraedu.com')]")

    # ── Google Maps iframe ─────────────────────────────────────────────────────
    MAPS_IFRAME = (By.XPATH,
        "//iframe[contains(@src,'google.com/maps') or contains(@src,'maps.google') or "
        "         contains(@title,'map') or contains(@title,'Map')]"
    )

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Action Methods ─────────────────────────────────────────────────────────

    def load(self, base_url: str) -> None:
        """Navigate to the contact page."""
        url = f"{base_url.rstrip('/')}/contact"
        logger.info("Loading ContactPage: %s", url)
        self.open(url)

    def get_page_heading(self) -> str:
        return self.wait_and_get_text(self.PAGE_HEADING)

    def fill_form(
        self,
        full_name: str = "",
        phone: str = "",
        email: str = "",
        subject: str = "",
        message: str = "",
    ) -> None:
        """
        Fill in all contact form fields. Pass empty string to leave a field blank.

        Args:
            full_name: Applicant's full name.
            phone: Phone number string.
            email: Email address string.
            subject: Subject / enquiry type.
            message: Free-text message body.
        """
        logger.info(
            "Filling contact form | name=%s | phone=%s | email=%s | subject=%s",
            full_name, phone, email, subject,
        )
        if full_name:
            self.safe_send_keys(self.FORM_FULL_NAME, full_name)
        if phone:
            self.safe_send_keys(self.FORM_PHONE, phone)
        if email:
            self.safe_send_keys(self.FORM_EMAIL, email)
        if subject:
            self.safe_send_keys(self.FORM_SUBJECT, subject)
        if message:
            self.safe_send_keys(self.FORM_MESSAGE, message)

    def fill_field(self, field_name: str, value: str) -> None:
        """
        Fill a single form field by logical name.

        Args:
            field_name: One of 'name', 'phone', 'email', 'subject', 'message'.
            value: Text to enter.
        """
        field_map = {
            "name":    self.FORM_FULL_NAME,
            "phone":   self.FORM_PHONE,
            "email":   self.FORM_EMAIL,
            "subject": self.FORM_SUBJECT,
            "message": self.FORM_MESSAGE,
        }
        locator = field_map.get(field_name.lower())
        if locator is None:
            raise ValueError(f"Unknown form field: '{field_name}'")
        logger.debug("Filling field '%s' with '%s'", field_name, value)
        self.safe_send_keys(locator, value)

    def submit_form(self) -> None:
        """Click the form submit button."""
        logger.info("Submitting contact form")
        self.safe_click(self.FORM_SUBMIT_BTN)

    def is_success_message_visible(self, timeout: int = 15) -> bool:
        """Return True if a success confirmation message appears after submit."""
        return self.is_element_visible(self.FORM_SUCCESS_MSG, timeout=timeout)

    def get_success_message_text(self) -> str:
        return self.wait_and_get_text(self.FORM_SUCCESS_MSG)

    def are_validation_errors_visible(self, timeout: int = 5) -> bool:
        """Return True if any custom validation error messages are visible."""
        return self.is_element_visible(self.VALIDATION_MSG_ANY, timeout=timeout)

    def get_html5_validation_message(self, field_locator: tuple) -> str:
        """
        Return the HTML5 browser-native validation message for a form field.
        Uses JavaScript to retrieve the `validationMessage` property.

        Args:
            field_locator: The (By.*, 'selector') locator of the input element.

        Returns:
            The native validation message string (may be empty if field is valid).
        """
        element = self.wait_for_element(field_locator)
        msg = self.driver.execute_script(
            "return arguments[0].validationMessage;", element
        )
        logger.debug("HTML5 validation message for %s: '%s'", field_locator, msg)
        return msg or ""

    def is_field_invalid(self, field_locator: tuple) -> bool:
        """
        Return True if the HTML5 constraint-validation API marks the field invalid.
        Uses JavaScript `validity.valid`.
        """
        element = self.wait_for_element(field_locator)
        is_valid = self.driver.execute_script(
            "return arguments[0].validity.valid;", element
        )
        return not is_valid

    def is_maps_iframe_present(self) -> bool:
        """Return True if the Google Maps embed iframe is present in the DOM."""
        return self.is_element_present(self.MAPS_IFRAME)

    def get_contact_phone_text(self) -> str:
        return self.wait_and_get_text(self.CONTACT_PHONE_TEXT)

    def get_contact_email_text(self) -> str:
        return self.wait_and_get_text(self.CONTACT_EMAIL_TEXT)

    def clear_form(self) -> None:
        """Clear all form fields (useful for sequential scenario steps)."""
        for locator in [
            self.FORM_FULL_NAME,
            self.FORM_PHONE,
            self.FORM_EMAIL,
            self.FORM_SUBJECT,
        ]:
            try:
                el = self.wait_for_visible(locator, timeout=3)
                el.clear()
            except Exception:
                pass
        try:
            el = self.wait_for_visible(self.FORM_MESSAGE, timeout=3)
            el.clear()
        except Exception:
            pass

    def is_form_visible(self) -> bool:
        return self.is_element_visible(self.FORM_SUBMIT_BTN)
