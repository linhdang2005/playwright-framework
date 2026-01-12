import pytest
import os, sys
from playwright.async_api import Page, expect
from pathlib import Path
from pytest_asyncio import fixture


#logging configuration
import logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#read test data
current_wd = os.getcwd()
sys.path.append(current_wd)
sys.path.append(os.path.join(current_wd, "utils"))
sys.path.append(os.path.join(current_wd, "common"))
sys.path.append(os.path.join(current_wd, "pages"))
from pages.voyage_form_page import search_voyage_form, bl_table
from pages.home_page import left_nav
from utils import common



#global variables
test_config = current_wd + "/test_data/config_voyage_form.json"
config_data = common.read_config(test_config)
test_data = config_data["voyage_form"]

#Test case: Import voyage form
@pytest.mark.asyncio
async def test_import_voyage_form(page: Page):
    test_case_data = test_data[0]
    voyage_page = search_voyage_form(page)
    nav_page = left_nav(page)
    imported_form = bl_table(page)
    try:
    # Navigate to Voyage Form page
        await nav_page.navigate_to_voyage_form()

    # Click on Import button to open the import dialog
        await voyage_page.click_import_voyage_form()

    # Upload the file
        file_path = str(Path("test_data/voyage_form_tempalte.xlsx").resolve())
        await voyage_page.set_input_files("//input[@type='file']", file_path)

        # Verify that the import was successful
        await page.reload()
        await expect(imported_form.row_voyage_form(test_case_data["voyage_form"]["voyage_form_filename"])).to_be_visible(timeout=10000)


    except Exception as e:
        logger.error(f"Test failed due to: {e}")
        assert False
    else:
        print("Test passed!")
        assert True

