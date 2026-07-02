

Feature: Courses Catalog Page
  As a prospective student on the SkillMantra courses page
  I want to see all available courses and filter them by category
  So that I can find the right program for my career goals

  Background:
    Given I am on the courses catalog page

  # Page load

  @smoke @courses
  Scenario: Verify courses catalog page loads successfully
    Then the courses page heading should be visible
    And the URL should contain "/courses"

  # Filter tabs 

  @regression @courses @filters
  Scenario: Verify all four category filter tabs are present
    Then the following filter tabs should be present:
      | tab_name               |
      | All Ecosystems         |
      | Software Engineering   |
      | Data Science           |
      | Infrastructure         |

  @regression @courses @filters
  Scenario Outline: Verify filtering by category shows matching courses
    When I click the "<category>" filter tab
    Then at least 1 course card should be visible
    And the filter tab "<category>" should appear active or selected

    Examples:
      | category               |
      | All Ecosystems         |
      | Software Engineering   |
      | Data Science           |
      | Infrastructure         |

  #Course card structure 

  @smoke @courses @cards
  Scenario: Verify at least one course card is shown on the catalog
    Then at least 1 course card should be visible

  @regression @courses @cards
  Scenario: Verify course cards contain duration information
    Then at least one course card should display duration or week information

  @regression @courses @cards
  Scenario: Verify course cards contain tech stack tags
    Then at least one course card should display technology tag chips

  @regression @courses @cards
  Scenario: Verify "View Syllabus" action is present on course cards
    Then at least one course card should have a "View Syllabus" link

  @regression @courses @cards
  Scenario: Verify "Configure Track" action is present on course cards
    Then at least one course card should have a "Configure Track" button

  #Configure Track navigation

  @smoke @courses @configure_track
  Scenario: Verify clicking "Configure Track" navigates to the contact/enquiry flow
    When I click the first available "Configure Track" button
    Then the URL should contain "/contact" or the page should scroll to a contact form
