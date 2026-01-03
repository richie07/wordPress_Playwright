from pages.base_page import BasePage

class UserPage(BasePage):
    """
    Page Object Model for the Users Page.
    """
    
    # Locators
    USERS_MENU_LINK = "#menu-users" # Or specific ID if available
    ADD_NEW_BUTTON = ".page-title-action" # "Add New" button near title
    USERNAME_INPUT = "#user_login"
    EMAIL_INPUT = "#email"
    ADD_USER_SUBMIT_BUTTON = "#createusersub"
    
    # Search locators
    SEARCH_INPUT = "#user-search-input"
    SEARCH_SUBMIT = "#search-submit"

    def navigate_to_users(self):
        """Navigate to the Users page via the sidebar menu."""
        # Assuming we are logged in, otherwise we might need to login first.
        # Use ID selector which is language independent
        self.page.click(self.USERS_MENU_LINK) 

    def start_add_new_user(self):
        """Click the 'Add New' button."""
        # In WP Admin users page, "Add New" is a link with class page-title-action
        self.click("a.page-title-action[href*='user-new.php']")

    def create_user(self, username: str, email: str):
        """Fill the add user form and submit."""
        self.fill_text(self.USERNAME_INPUT, username)
        self.fill_text(self.EMAIL_INPUT, email)
        # We might need to handle password toggles if mandatory, 
        # but often WP allows adding without password (sends email) or generates one.
        # Let's assume standard flow.
        # Sometimes there's a checkbox "Send User Notification" checked by default.
        
        # Click "Add New User" button
        self.click(self.ADD_USER_SUBMIT_BUTTON)

    def search_user(self, username: str):
        """Search for a user in the list."""
        self.fill_text(self.SEARCH_INPUT, username)
        self.click(self.SEARCH_SUBMIT)

    def is_user_visible(self, username: str) -> bool:
        """Check if user needs to be searchable or just visible in the list."""
        # Simple check: search and see if a link with the username exists
        # self.search_user(username) 
        # Using a locator that looks for the username link in the table
        return self.page.is_visible(f"table.users tr td.username a:text('{username}')")

    def delete_user(self, username: str):
        """Delete a user."""
        # First ensure user is visible
        if not self.is_user_visible(username):
            return # Or raise error
        
        # Hover over the row to reveal actions
        row_selector = f"table.users tr:has(td.username a:text('{username}'))"
        self.page.locator(row_selector).hover()
        
        # Click "Delete"
        # It's usually a link with class 'submitdelete'
        self.page.click(f"{row_selector} .submitdelete")
        
        # New page usually appears: "Delete Users". Confirm deletion.
        # "Confirm Deletion" button
        if self.page.is_visible("#submit"):
            self.click("#submit")

    def ensure_user_exists(self, username: str, email: str):
        """Helper to create user if not exists."""
        # Navigate to users, search. If not found, add.
        # self.navigate_to_users() # Assume already there or managed by step
        if not self.is_user_visible(username):
            self.start_add_new_user()
            self.create_user(username, email)
            # wait for return to list
            self.page.wait_for_selector(self.SEARCH_INPUT) 
