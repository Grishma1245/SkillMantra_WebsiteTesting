

Feature: Site Navigation
  As a visitor to SkillMantra
  I want all navigation links to work correctly
  So that I can discover courses and contact the academy without dead-ends

  Background:
    Given I am on the SkillMantra homepage

  #Primary navigation bar 

  @smoke @navigation
  Scenario: Verify homepage loads successfully with correct title
    Then the page title should contain "SkillMantra"

  @smoke @navigation
  Scenario: Verify "Courses" nav link navigates to the courses catalog
    When I click the "Courses" navigation link
    Then the URL should contain "/courses"
    And the page should not return an error status

  @regression @navigation
  Scenario: Verify "Instructor" nav link navigates correctly
    When I click the "Instructor" navigation link
    Then the URL should contain "/instructor"
    And the page should not return an error status

  @regression @navigation
  Scenario: Verify "Placement" nav link navigates correctly
    When I click the "Placement" navigation link
    Then the URL should contain "/placement"
    And the page should not return an error status

  @regression @navigation
  Scenario: Verify "Blog" nav link navigates correctly
    When I click the "Blog" navigation link
    Then the URL should contain "/blog"
    And the page should not return an error status

  @regression @navigation
  Scenario: Verify "Contact" nav link navigates correctly
    When I click the "Contact" navigation link
    Then the URL should contain "/contact"
    And the page should not return an error status

  @regression @navigation
  Scenario: Verify "About" nav link navigates correctly
    When I click the "About" navigation link
    Then the URL should contain "/about"
    And the page should not return an error status

  #Top-bar corporate links
  @regression @navigation
  Scenario: Verify "Corporate Training" top-bar link navigates correctly
    When I click the "Corporate Training" top bar link
    Then the URL should contain "/corporate"
    And the page should not return an error status

  @regression @navigation
  Scenario: Verify "Corporate Analytics Service" top-bar link navigates correctly
    When I click the "Corporate Analytics Service" top bar link
    Then the URL should contain "/analysis"
    And the page should not return an error status

  # ── Footer domain links 

  @regression @navigation
  Scenario: Verify footer "Top Domains" links are present
    # KNOWN ISSUE: Footer links point to "#courses" anchor fragments on the homepage,
    # NOT to real sub-routes. We assert their presence and actual href values rather
    # than testing full-page navigation, to avoid hardcoding a false pass.
    Then the footer should contain at least one top-domain link
    And the footer top-domain links should point to the courses anchor

  # ── WhatsApp widget 

  @smoke @navigation @whatsapp
  Scenario: Verify floating WhatsApp "Core Advisor" widget is visible
    Then the WhatsApp chat widget should be visible on the page

  @regression @navigation @whatsapp
  Scenario: Verify clicking "Initialize Secure Chat" opens WhatsApp in a new tab
    When I click the WhatsApp chat widget
    And I click the "Initialize Secure Chat" button
    Then a new browser tab should open with a URL containing "api.whatsapp.com"
    And I switch back to the original tab
