import pytest
import os, sys
from playwright.async_api import expect
from pages.profile_page import profilepage
from pages.login_page import loginpage
from pages.search_book_page import bookpage
from api.add_book_api import add_books
from api.generate_token_api import generate_token


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
async def test_search_book(logged_in_page):
    page_book = bookpage(logged_in_page)
    
    try:
    #search with keyword 1 and verify result
        await page_book.search_book(test_data_search["keyword1"])
    
        # Count result return
        keyword1 = test_data_search["keyword1"]
        results_1 = page_book.result_titles
        count_1 = await results_1.count()
        print (f'total results: {count_1}')
        # Verify result return match with keyword
        for i in range(count_1):
            title_text_1 = await results_1.nth(i).inner_text()
            assert keyword1.lower() in title_text_1.lower()

    #search with keyword 2 and verify result
        await page_book.search_book(test_data_search["keyword2"])
    
        # Count result return
        keyword2 = test_data_search["keyword2"]
        results_2 = page_book.result_titles
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


  # add books first via API
def test_add_books_api():
    token = generate_token()
    add_books(token)

#Scenario 2: Delete book successfully
# @pytest.mark.skip
async def test_delete_book(logged_in_page):
    profile_page = profilepage(logged_in_page)

    try:
    # Acces to profile page
        await profile_page.navigate_to_profile()
    # User Search book: Leaning JavaScript Design Patterns
        await profile_page.search_book(test_data_book["book1"])
    # Delete book
        await profile_page.delete_book_button.click()

        # Handle alert popup
        async with logged_in_page.expect_event("dialog") as dialog_info:
            await profile_page.confirm_delete_button.click()
        dialog = await dialog_info.value
        await dialog.accept()

    # Verify result
        await expect(profile_page.no_rows_found).to_be_visible()

    except Exception as e:
        logger.error(f"Test failed due to: {e}")
        assert False
    else:
        print("Test passed!")
        assert True
