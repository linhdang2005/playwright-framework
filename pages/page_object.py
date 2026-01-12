from playwright.async_api import Page
from playwright.async_api import expect


class searchbl:
    def __init__(self, page: Page):
        self.page = page
        # Textbox
        self.vessel = page.get_by_placeholder("Search vessels...")          # placeholder từ ảnh
        self.voyage = page.get_by_placeholder("Search or enter voyage...")
        self.port_agent = page.get_by_placeholder("Search port agents...")
        self.bl_number = page.get_by_placeholder("Enter BL number...")
        # Dropdown
        self.source = page.locator('div').filter(has_text='Source').get_by_role('combobox')

        # Buttons
        self.btn_search = page.get_by_role("button", name="Search")
        self.btn_clear  = page.get_by_role("button", name="Clear")
        self.btn_export_excel = page.get_by_role("button", name="Export Excel")
        self.btn_edit_mode = page.get_by_role("button", name="Edit Mode")
        self.btn_exit_edit_mode = page.get_by_role("button", name="Exit Edit Mode")

        #Checkboxes



    async def fill_vessel(self, text: str):
        await self.vessel.fill(text)

    async def fill_voyage(self, text: str):
        await self.voyage.fill(text)

    async def fill_port_agent(self, text: str):
        await self.port_agent.fill(text)

    async def select_source(self, option: str):
        await self.source.select_option(label=option)

    async def fill_bl_number(self, text: str):
        await self.bl_number.fill(text)

    async def click_search_btn(self):
        await self.btn_search.click()
        await self.page.wait_for_load_state("networkidle")

    async def click_clear_btn(self):
        await self.btn_clear.click()
        await self.page.wait_for_load_state("networkidle")

    async def clear_search_box(self):
        await self.btn_clear.click()
        await expect(self.vessel).to_be_empty()
        await expect(self.voyage).to_be_empty()
        await expect(self.port_agent).to_be_empty()
        await expect(self.bl_number).to_be_empty()

    async def export_excel(self):
        # xử lý download
        async with self.page.expect_download() as dl:
            await self.btn_export.click()
        download = await dl.value
        return await download.path()
    
    async def click_edit_mode_btn(self):
        await self.btn_edit_mode.click()
        await expect(self.page.get_by_text("Edit Mode Active:")).to_be_visible()

    async def click_exit_edit_mode_btn(self):
        await self.btn_edit_mode.click()
        await expect(self.page.get_by_text("Edit Mode deactivated")).to_be_visible()



class bl_table:
    def __init__(self, page: Page):
        self.page = page
        self.table = page.locator("table") 

        #Checkbox on the  table
        self.checkbox = page.get_by_role("checkbox")

    #find bl_no in table rows
    def row_by_bl_no(self, bl_no: str):
        return self.page.locator("tr", has=self.page.get_by_text(bl_no).first)
    
    #assert bl table is present
    async def assert_bl_present(self):
        await expect(self.table).to_be_visible()
   
    #check bl_no present in table

    async def count_rows(self) -> int:
        return await self.page.locator("tbody tr").count()