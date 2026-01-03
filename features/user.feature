@user
Feature: User Management
    As an Admin
    I want to manage users
    So that I can control access to the site

    Scenario: Create a new user
        Given I am logged in as Admin
        And I am on the Users page
        When I create a new user with username "newuser" and email "newuser@example.com"
        Then the user "newuser" should appear in the user list

    Scenario: Delete a user
        Given I am logged in as Admin
        And I am on the Users page
        And a user "user_to_delete" exists
        When I delete the user "user_to_delete"
        Then the user "user_to_delete" should not appear in the user list
