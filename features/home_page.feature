

Feature: Homepage Content and Interactions
  As a prospective student visiting the SkillMantra homepage
  I want to see all key sections and be able to interact with them
  So that I understand what the academy offers and can take action

  Background:
    Given I am on the SkillMantra homepage

  #Hero Section

  @smoke @homepage
  Scenario: Verify hero section loads with headline and CTA buttons
    Then the hero headline should be visible
    And the "Explore Programs" CTA button should be visible
    And the "Consult Career Architect" CTA button should be visible

  @smoke @homepage
  Scenario: Verify hero section displays correct headline text
    Then the hero headline should contain "Master Technical Frontiers"

  # ── Stats / Metrics

  @regression @homepage
  Scenario: Verify stats section displays rating, Live Labs and Doubt Sync metrics
    Then the stats section should show "4.8*" global rating
    And the stats section should show "100%" for Live Labs
    And the stats section should show "24x7" for Doubt Sync

  # ── Course Preview Cards 
  @regression @homepage
  Scenario: Verify Data Science course preview card is visible
    Then the course card for "Data Science Engineering" should be visible

  @regression @homepage
  Scenario: Verify DevOps course preview card is visible
    Then the course card for "DevOps" should be visible

  @regression @homepage
  Scenario: Verify QA Automation course preview card is visible
    Then the course card for "QA" should be visible

  @regression @homepage
  Scenario: Verify all three hero course preview cards are rendered
    Then at least 3 course preview cards should be visible in the hero panel

  # ── CTA Button Behaviour 
  @regression @homepage
  Scenario: Verify "Explore Programs" CTA scrolls to or navigates to courses section
    When I click the "Explore Programs" button
    Then the page URL should contain "#courses" or the courses section should be in view

  @regression @homepage
  Scenario: Verify "Consult Career Architect" CTA scrolls to contact section
    When I click the "Consult Career Architect" button
    Then the URL should contain "#contact" or the contact section should be in view

  #Lead Form 

  @smoke @homepage @lead_form
  Scenario: Verify lead form "Get Customized Course Guidance" section is present
    Then the lead form section should be present on the page

  @regression @homepage @lead_form
  Scenario: Verify lead form program checkboxes are visible
    When I scroll to the contact section
    Then the Full Stack program option should be visible in the lead form
    And the ML Engineer program option should be visible in the lead form
    And the QA Testing Automation Track option should be visible in the lead form
    And the lead form submit button should be visible
