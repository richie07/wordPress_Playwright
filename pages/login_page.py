from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    """
    Page Object Model for the Login Page.
    Inherits from BasePage to access shared Playwright wrappers.
    """
    
    # Locators
    USERNAME_INPUT = "#user_login"
    PASSWORD_INPUT = "#user_pass"
    LOGIN_BUTTON = "#wp-submit"
    ERROR_MESSAGE = "#login_error"  # Helper for robust testing of failure cases
    SUCCESS_INDICATOR = "#wpadminbar" # Used to verify successful login

    def __init__(self, page):
        super().__init__(page)
        self.url = Config.get_base_url()

    def navigate_to_login(self):
        """Go to the login page."""
        self.navigate(self.url)

    def do_login(self, username, password):
        """Perform the login action."""
        self.fill_text(self.USERNAME_INPUT, username)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message_text(self):
        """Retrieve error text if login failed."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None

    def is_login_successful(self):
        """Check if login was successful by looking for a dashboard element."""
        try:
            self.wait_for_selector(self.SUCCESS_INDICATOR, timeout=3000)
            return True
        except:
            return False
