import pytest
import time
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage
from pages.user_page import UserPage
from playwright.sync_api import Page, expect

# Load scenarios
scenarios('user.feature')

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture
def user_page(page: Page):
    return UserPage(page)

# Shared Steps
@given('I am logged in as Admin')
def login_as_admin(login_page):
    login_page.navigate_to_login()
    login_page.do_login("Admin", "admin_password")
    assert login_page.is_login_successful(), "Failed to login as Admin"

@given('I am on the Users page')
def navigate_to_users(user_page):
    user_page.navigate_to_users()

# Scenario 1: Create User
@when(parsers.parse('I create a new user with username "{username}" and email "{email}"'))
def create_new_user(user_page, username, email):
    # Ensure user logic - if it exists maybe delete it first? 
    # For now assume fresh or handle manually
    if user_page.is_user_visible(username):
        user_page.delete_user(username)
    
    user_page.start_add_new_user()
    user_page.create_user(username, email)

@then(parsers.parse('the user "{username}" should appear in the user list'))
def verify_user_created(user_page, username):
    # Wait a bit for list refresh if needed
    time.sleep(1) 
    assert user_page.is_user_visible(username), f"User {username} was not found in the list"

# Scenario 2: Delete User
@given(parsers.parse('a user "{username}" exists'))
def ensure_user_exists(user_page, username):
    # We need a valid email to create. Let's fake one.
    email = f"{username}@example.com"
    user_page.ensure_user_exists(username, email)

@when(parsers.parse('I delete the user "{username}"'))
def delete_user(user_page, username):
    user_page.delete_user(username)

@then(parsers.parse('the user "{username}" should not appear in the user list'))
def verify_user_deleted(user_page, username):
    assert not user_page.is_user_visible(username), f"User {username} still exists after deletion"
