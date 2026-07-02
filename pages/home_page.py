"""
home_page.py
------------
Page Object for the SkillMantra homepage (https://skillmantraedu.com/).

All locators are defined here; step definitions must NOT contain any selectors.
Locators are derived from the live DOM (Tailwind-based, no ID-heavy structure).
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Page Object for the SkillMantra homepage."""

    # ── Hero Section Locators ──────────────────────────────────────────────────
    HERO_SECTION         = (By.CSS_SELECTOR, "section.bg-gradient-to-br.from-logoBlueDark")
    HERO_HEADLINE        = (By.CSS_SELECTOR, "section h1")
    EXPLORE_PROGRAMS_BTN = (By.XPATH, "//a[normalize-space()='Explore Programs']")
    CONSULT_CAREER_BTN   = (By.XPATH, "//a[normalize-space()='Consult Career Architect']")

    # ── Stats / Metrics Section ────────────────────────────────────────────
    # The live DOM uses h4 elements: <h4>4.8★</h4>  <h4>100%</h4>  <h4>24x7</h4>
    # We match on the numeric prefix to avoid Unicode encoding issues in selectors.
    STAT_RATING     = (By.XPATH, "//h4[starts-with(normalize-space(),'4.8')]")
    STAT_LIVE_LABS  = (By.XPATH, "//h4[contains(normalize-space(),'100%')]")
    STAT_DOUBT_SYNC = (By.XPATH, "//h4[contains(normalize-space(),'24x7')]")

    # ── Course Preview Cards (hero panel) ─────────────────────────────────────
    HERO_COURSE_CARDS    = (By.CSS_SELECTOR, "div.bg-logoBlueDeep.border.border-white\\/5.p-4.rounded-xl")
    HERO_CARD_DATA_SCI   = (By.XPATH, "//h5[contains(text(),'Data Science Engineering')]")
    HERO_CARD_DEVOPS     = (By.XPATH, "//h5[contains(text(),'DevOps')]")
    HERO_CARD_QA         = (By.XPATH, "//h5[contains(text(),'QA')]")
    HERO_CARD_VIEW_BTN   = (By.XPATH,
        "//h5[contains(text(),'Data Science Engineering')]"
        "/ancestor::div[contains(@class,'p-4')]"
        "//a[contains(text(),'View') or contains(text(),'view')]"
    )

    # Generic "View" button inside any hero card — first match
    HERO_ANY_VIEW_BTN = (By.XPATH,
        "//div[contains(@class,'bg-logoBlueDeep') and contains(@class,'p-4')]"
        "//a[normalize-space()='View Details' or normalize-space()='View' or "
        "     normalize-space()='Enroll' or @href='#contact' or @href='/contact']"
    )

    # ── Course Section (below hero) ────────────────────────────────────────────
    COURSES_SECTION = (By.CSS_SELECTOR, "section#courses, section[id='courses'], div#courses")

    # ── Testimonials ──────────────────────────────────────────────────────────
    TESTIMONIAL_CARDS    = (By.XPATH, "//div[contains(@class,'testimonial') or .//p[@class and contains(.,'reviewer')]]")
    # More reliable: look for any card block containing a star rating + reviewer name
    TESTIMONIAL_REVIEWER = (By.XPATH, "//p[contains(@class,'font-bold') and ancestor::div[.//i[contains(@class,'bi-star')]]]")

    # ── Lead Form "Get Customized Course Guidance" ────────────────────────────
    LEAD_FORM_SECTION    = (By.CSS_SELECTOR, "section#contact")
    LEAD_FORM_HEADING    = (By.XPATH, "//section[@id='contact']//*[contains(text(),'Get Customized Course Guidance')]")
    LEAD_FORM_NAME       = (By.CSS_SELECTOR, "#leadAdvisoryForm input[name='full_name']")
    LEAD_FORM_EMAIL      = (By.CSS_SELECTOR, "#leadAdvisoryForm input[name='email_address']")
    LEAD_FORM_PHONE      = (By.CSS_SELECTOR, "#leadAdvisoryForm input[name='phone_number']")
    LEAD_FORM_PROGRAM_SELECT = (By.CSS_SELECTOR, "#leadAdvisoryForm select[name='selected_program']")
    LEAD_FORM_SUBMIT_BTN = (By.CSS_SELECTOR, "#leadAdvisoryForm button[type='submit']")

    # Select options inside the program dropdown
    LEAD_FORM_CHECKBOX_FULLSTACK = (By.XPATH, "//select[@name='selected_program']/option[contains(text(),'Full Stack')]")
    LEAD_FORM_CHECKBOX_ML        = (By.XPATH, "//select[@name='selected_program']/option[contains(text(),'ML Engineer')]")
    LEAD_FORM_CHECKBOX_QA        = (By.XPATH, "//select[@name='selected_program']/option[contains(text(),'QA Testing Automation')]")

    # Success message after form submission
    FORM_SUCCESS_MSG = (By.XPATH,
        "//*[contains(normalize-space(),'Transmission Successful') or "
        "    contains(normalize-space(),'Successfully') or "
        "    contains(normalize-space(),'Thank you')]"
    )

    # ── WhatsApp floating widget ───────────────────────────────────────────────
    # The button to toggle the drawer (specifically matching the floating launcher button, not the close button inside the drawer)
    WHATSAPP_WIDGET_BTN   = (By.XPATH, "//button[contains(@onclick, 'toggleWaDrawer') and contains(@class, 'bg-emerald-500')]")
    # The direct routing anchor inside the toggle drawer
    WHATSAPP_CHAT_INIT_BTN = (By.CSS_SELECTOR, "#waDirectRoutingAnchor")

    # ── Navigation Links (also on all pages) ──────────────────────────────────
    NAV_COURSES    = (By.XPATH, "//nav//a[@href='/courses' and normalize-space()='Courses']")
    NAV_INSTRUCTOR = (By.XPATH, "//nav//a[@href='/instructor']")
    NAV_PLACEMENT  = (By.XPATH, "//nav//a[@href='/placement']")
    NAV_BLOG       = (By.XPATH, "//nav//a[@href='/blog']")
    NAV_CONTACT    = (By.XPATH, "//nav//a[@href='/contact']")
    NAV_ABOUT      = (By.XPATH, "//nav//a[@href='/about']")

    # Top bar / global header links
    TOP_BAR_CORPORATE      = (By.XPATH, "//a[@href='/corporate']")
    TOP_BAR_ANALYTICS_SVC  = (By.XPATH, "//a[@href='/analysis']")

    # Footer top-domains section
    # Known issue: these links point to #courses anchors, not real routes
    FOOTER_TOP_DOMAIN_LINKS = (By.XPATH,
        "//footer//a[contains(@href,'#courses') or contains(@href,'courses')]"
    )

    # ── Page heading / title verification ─────────────────────────────────────
    PAGE_TITLE_TAG = (By.CSS_SELECTOR, "title")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Action Methods ─────────────────────────────────────────────────────────

    def load(self, base_url: str) -> None:
        """Navigate to the homepage."""
        logger.info("Loading HomePage: %s", base_url)
        self.open(base_url)

    def is_hero_headline_visible(self) -> bool:
        return self.is_element_visible(self.HERO_HEADLINE)

    def get_hero_headline_text(self) -> str:
        return self.wait_and_get_text(self.HERO_HEADLINE)

    def is_explore_programs_btn_visible(self) -> bool:
        return self.is_element_visible(self.EXPLORE_PROGRAMS_BTN)

    def is_consult_career_btn_visible(self) -> bool:
        return self.is_element_visible(self.CONSULT_CAREER_BTN)

    def get_stat_rating_text(self) -> str:
        return self.wait_and_get_text(self.STAT_RATING)

    def get_stat_live_labs_text(self) -> str:
        return self.wait_and_get_text(self.STAT_LIVE_LABS)

    def get_stat_doubt_sync_text(self) -> str:
        return self.wait_and_get_text(self.STAT_DOUBT_SYNC)

    def is_data_science_card_visible(self) -> bool:
        return self.is_element_visible(self.HERO_CARD_DATA_SCI)

    def is_devops_card_visible(self) -> bool:
        return self.is_element_visible(self.HERO_CARD_DEVOPS)

    def is_qa_card_visible(self) -> bool:
        return self.is_element_visible(self.HERO_CARD_QA)

    def click_explore_programs(self) -> None:
        """Click 'Explore Programs' CTA → should scroll/navigate to #courses."""
        logger.info("Clicking 'Explore Programs' button")
        self.safe_click(self.EXPLORE_PROGRAMS_BTN)

    def click_consult_career(self) -> None:
        """Click 'Consult Career Architect' → scrolls to #contact section."""
        logger.info("Clicking 'Consult Career Architect' button")
        self.safe_click(self.CONSULT_CAREER_BTN)

    def is_lead_form_visible(self) -> bool:
        return self.is_element_visible(self.LEAD_FORM_SECTION)

    def scroll_to_contact_section(self) -> None:
        self.scroll_to_locator(self.LEAD_FORM_SECTION)

    def is_whatsapp_widget_visible(self) -> bool:
        return self.is_element_visible(self.WHATSAPP_WIDGET_BTN)

    def click_whatsapp_widget(self) -> None:
        logger.info("Clicking WhatsApp widget / Core Advisor button")
        self.safe_click(self.WHATSAPP_WIDGET_BTN)

    def click_initialize_chat(self) -> str:
        """
        Click 'Initialize Secure Chat'. Returns the original window handle
        so the caller can switch back after inspecting the new tab.
        """
        original_handle = self.get_current_window_handle()
        logger.info("Clicking 'Initialize Secure Chat'")
        self.safe_click(self.WHATSAPP_CHAT_INIT_BTN)
        return original_handle

    def count_hero_course_cards(self) -> int:
        return self.count_elements(self.HERO_COURSE_CARDS)
