

Feature: Contact Form Validation and Submission
  As a prospective student on the SkillMantra contact page
  I want the contact form to validate inputs and confirm successful submission
  So that I can reach out to advisors with confidence

  Background:
    Given I am on the contact page

  # ── Positive: successful submission ───────────────────────────────────────

  @smoke @contact @positive
  Scenario: Submit the contact form with valid data and verify success confirmation
    When I fill in the contact form with:
      | field   | value                          |
      | name    |Grishma Acharya                 |
      | phone   | +977 9843000001                |
      | email   | grishma.ach@testmail.com      |
      | subject | Course Enquiry - Data Science  |
      | message | I am interested in the Data Science Engineering programme. Please send me the syllabus and fee structure. |
    And I submit the contact form
    Then the success confirmation message should appear

  # ── Negative: empty required fields ───────────────────────────────────────

  @regression @contact @negative @validation
  Scenario Outline: Validate required field error when a field is left empty
    When I submit the contact form without filling in "<field>"
    Then the form should indicate "<field>" is required

    Examples:
      | field   |
      | name    |
      | phone   |
      | email   |
      | message |

  # ── Negative: invalid email format ────────────────────────────────────────

  @regression @contact @negative @validation
  Scenario Outline: Validate rejection of invalid email format
    When I fill in the contact form with:
      | field   | value                 |
      | name    | Test User             |
      | phone   | +977 9800000000       |
      | email   | <invalid_email>       |
      | subject | Test Subject          |
      | message | Testing invalid email |
    And I submit the contact form
    Then the form should show an email validation error

    Examples:
      | invalid_email       |
      | notanemail          |
      | missing@            |
      | @nodomain.com       |
      | plaintext           |

  # ── Negative: invalid phone format ────────────────────────────────────────

  @regression @contact @negative @validation
  Scenario Outline: Validate rejection of invalid phone number
    When I fill in the contact form with:
      | field   | value                  |
      | name    | Test User              |
      | phone   | <invalid_phone>        |
      | email   | valid@testmail.com     |
      | subject | Test Subject           |
      | message | Testing invalid phone  |
    And I submit the contact form
    Then the form should show a phone validation error or reject the submission

    Examples:
      | invalid_phone |
      | abc           |
      | 12            |
      | !@#$%^        |

  # ── Boundary: max-length message field ────────────────────────────────────

  @regression @contact @boundary
  Scenario: Verify message field accepts very long input without crashing
    When I fill in the contact form with:
      | field   | value                                                                                          |
      | name    | Boundary Tester                                                                                |
      | phone   | +977 9800000099                                                                                |
      | email   | boundary@testmail.com                                                                          |
      | subject | Boundary Test                                                                                  |
      | message | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA |
    And I submit the contact form
    Then the page should not crash or display a server error

  # ── Security smoke: XSS injection in message field ────────────────────────

  @regression @contact @security
  Scenario: Verify XSS script injection string in Message is sanitized and not executed
    When I fill in the contact form with:
      | field   | value                                                             |
      | name    | XSS Tester                                                       |
      | phone   | +977 9800000088                                                  |
      | email   | xss@testmail.com                                                 |
      | subject | Security Test                                                    |
      | message | <script>alert('XSS-1')</script><img src=x onerror=alert('XSS-2')> |
    And I submit the contact form
    Then no JavaScript alert dialog should appear
    And the page should not execute the injected script

  # ── Contact details verification ───────────────────────────────────────────

  @regression @contact @contact_details
  Scenario: Verify office phone number is displayed correctly
    Then the contact page should display phone number "+977 9843095969"

  @regression @contact @contact_details
  Scenario: Verify office email address is displayed correctly
    Then the contact page should display email "info@skillmantraedu.com"

  # ── Google Maps embed ──────────────────────────────────────────────────────

  @regression @contact @maps
  Scenario: Verify Google Maps embed iframe is present on the contact page
    Then the Google Maps iframe should be present on the page
