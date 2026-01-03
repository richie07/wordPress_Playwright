@login
Feature: WordPress Login
    As a user
    I want to login to the WordPress Dashboard
    So that I can manage my site

    Scenario: Successful Login
        Given I am on the WordPress login page
        When I enter valid credentials "Admin" and "admin_password"
        Then I should see the dashboard

    Scenario: Failed Login with invalid password
        Given I am on the WordPress login page
        When I enter user "Admin" and wrong password "wrongpass"
        Then I should see an error message
