from playwright.sync_api import Page, Locator, expect
from utils.logger import setup_logger

class BasePage:
    """
    Wrapper class for Playwright Page object.
    Centralizes all interactions with the browser to allow easier maintenance.
    """

    def __init__(self, page: Page):
        self.page = page
        self.logger = setup_logger(self.__class__.__name__)

    def navigate(self, url: str):
        """Navigate to the given URL."""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def find_element(self, selector: str) -> Locator:
        """Return a Locator object for the given selector."""
        return self.page.locator(selector)

    def click(self, selector: str):
        """Click on an element identified by the selector."""
        self.logger.info(f"Clicking on element: {selector}")
        self.find_element(selector).click()

    def fill_text(self, selector: str, text: str):
        """Fill an input field identified by the selector with text."""
        # Masking password in logs for security
        display_text = "*****" if "pass" in selector.lower() or "secret" in selector.lower() else text
        self.logger.info(f"Filling text '{display_text}' into: {selector}")
        self.find_element(selector).fill(text)

    def get_text(self, selector: str) -> str:
        """Get the inner text of an element."""
        self.logger.info(f"Getting text from: {selector}")
        return self.find_element(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        visible = self.find_element(selector).is_visible()
        self.logger.info(f"Checking visibility of '{selector}': {visible}")
        return visible

    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Wait for an element to appear in the DOM."""
        self.logger.info(f"Waiting for selector: {selector} (timeout={timeout}ms)")
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def get_title(self) -> str:
        """Get the page title."""
        title = self.page.title()
        self.logger.info(f"Page title is: {title}")
        return title
