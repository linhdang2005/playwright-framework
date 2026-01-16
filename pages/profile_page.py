from playwright.async_api import Page
class profilepage:
    def __init__(self, page: Page):
        self.page = page
        self.nav_profile = page.locator("//span[contains(text(), 'Profile')]")
        self.search_box = page.locator("#searchBox")
        self.search_button = page.locator("#basic-addon2")
        self.delete_book_button = page.locator("#delete-record-undefined")
        self.confirm_delete_button = page.get_by_role("button", name="OK")
        self.no_rows_found = page.locator("//div[contains(text(), 'No rows found')]")
    async def navigate_to_profile(self):
        await self.nav_profile.click()
    async def search_book(self, keyword):
        await self.search_box.fill(keyword)
        await self.search_button.click()