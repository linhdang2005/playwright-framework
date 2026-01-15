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
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from utils import common


#global variables
config_data = common.read_config(
    os.path.join(PROJECT_ROOT, "test_data", "config_test_data.json")
)
test_data_search = config_data["keyword"]
test_data_book= config_data["book"]

# @pytest.mark.skip
#Scenario 1: Search book with multiple results
@pytest.mark.asyncio
async def test_search_book(page):
    try:
    # Input keyword 1
        await page.locator("#searchBox").fill(test_data_search["keyword1"])
    # Click on search button
        await page.locator("#basic-addon2").click()
    # Count result return
        keyword1 = test_data_search["keyword1"]
        results_1 = page.locator("div.action-buttons a")
        count_1 = await results_1.count()
        print (f'total results: {count_1}')
    # Verify result return match with keyword
        for i in range(count_1):
            title_text_1 = await results_1.nth(i).inner_text()
            assert keyword1.lower() in title_text_1.lower()

    # Input keyword 2
        await page.locator("#searchBox").fill(test_data_search["keyword2"])
    # Click on search button
        await page.locator("#basic-addon2").click()
    # Count result return
        keyword2 = test_data_search["keyword2"]
        results_2 = page.locator("div.action-buttons a")
        count_2 = await results_2.count()
        print (f'total results: {count_2}')
    # Verify result return match with keyword
        for i in range(count_2):
            title_text_2 = await results_2.nth(i).inner_text()
            assert keyword2.lower() in title_text_2.lower()

    except Exception as e:
        logger.error(f"Test failed due to: {e}")
        assert False
    else:
        print("Test passed!")
        assert True


#Scenario 2: Delete book successfully

async def test_delete_book(page):
    try:
    # Acces to profile page
        await page.locator("//span[contains(text(), 'Profile')]").click()
        # await page.wait_for_load_state("networkidle")
    # User Search book: Leaning JavaScript Design Patterns
        await page.locator("#searchBox").fill(test_data_book["book1"])
        await page.locator("#basic-addon2").click()
    # Delete book
        await page.locator("#delete-record-undefined").click()

        # Handle alert popup
        async with page.expect_event("dialog") as dialog_info:
         await page.get_by_role("button", name="OK").click()
        dialog = await dialog_info.value
        await dialog.accept()

    # Verify result
        await expect(page.locator("//div[contains(text(), 'No rows found')]")).to_be_visible()

    except Exception as e:
        logger.error(f"Test failed due to: {e}")
        assert False
    else:
        print("Test passed!")
        assert True
