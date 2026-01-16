
from playwright.async_api import Page

class loginpage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#userName")
        self.password = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")
        self.login_username_display = page.locator("#userName-value")