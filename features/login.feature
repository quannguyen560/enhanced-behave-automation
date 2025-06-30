@fixture.chrome
Feature: Login Functionality

  Background:
    Given User navigates to login page

  @smoke @login
  Scenario: Successful login with valid credentials
    Given User is on the login page
    When User enters username "testuser@example.com"
    And User enters password "ValidPassword123"
    And User clicks login button
    Then User should be redirected to dashboard
    And User should see welcome message

  @negative @login
  Scenario: Login with invalid credentials
    Given User is on the login page
    When User enters username "invalid@example.com"
    And User enters password "InvalidPassword"
    And User clicks login button
    Then User should see error message "Invalid credentials"
    And User should remain on login page

  @multilang @login
  Scenario Outline: Multi-language login validation
    Given The test is configured for <language> language
    And User is on the login page
    When User clicks the login button without entering credentials
    Then User should see <error_type> validation message

    Examples:
      | language   | error_type |
      | english    | required   |
      | vietnamese | required   |

  @security @login
  Scenario: Password field masking
    Given User is on the login page
    When User enters password "SecretPassword123"
    Then Password field should be masked
    And Password text should not be visible

  @functionality @login
  Scenario: Remember me functionality
    Given User is on the login page
    When User enters valid credentials
    And User checks "Remember me" option
    And User clicks login button
    Then User should be logged in
    When User closes browser and reopens
    Then User should still be logged in

  @responsive @login
  Scenario: Login page responsive design
    Given User is on the login page
    When User resizes browser to mobile view
    Then Login form should be responsive
    And All elements should be visible and functional