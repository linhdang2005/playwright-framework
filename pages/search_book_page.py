from playwright.async_api import Page
class bookpage:
    def __init__(self, page: Page):
        self.page = page
        self.search_box = page.locator("#searchBox")
        self.search_button = page.locator("#basic-addon2")
        self.result_titles = page.locator("div.action-buttons a")

    async def search_book(self, keyword: str):
        await self.search_box.fill(keyword)
        await self.search_button.click()  