import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage
from playwright.sync_api import Page, expect

# Constants
# Ideally these should come from environment variables or a config file
VALID_USER = "user"
VALID_PASSWORD = "password"

# Load scenarios from the feature file
scenarios('login.feature')

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@given('I am on the WordPress login page')
def open_login_page(login_page):
    login_page.navigate_to_login()

@when(parsers.parse('I enter valid credentials "{username}" and "{password}"'))
def enter_valid_credentials(login_page, username, password):
    # In a real scenario, you might ignore the arguments if you use env vars, 
    # but here we follow the feature file for demonstration
    login_page.do_login(username, password)

@when(parsers.parse('I enter user "{username}" and wrong password "{password}"'))
def enter_invalid_credentials(login_page, username, password):
    login_page.do_login(username, password)

@then('I should see the dashboard')
def verify_dashboard_visible(login_page):
    assert login_page.is_login_successful(), "Dashboard was not visible after login"

@then('I should see an error message')
def verify_error_message(login_page):
    error_text = login_page.get_error_message_text()
    assert error_text is not None, "Error message was not displayed"
    assert "Error" in error_text or "Lost your password" in error_text or "is incorrect" in error_text # Loose check for standard WP errors
