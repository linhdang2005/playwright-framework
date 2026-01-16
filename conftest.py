import pytest
from playwright.async_api import async_playwright
from utils.common import login_user
import os, sys



@pytest.fixture(scope="function")
async def browser():
    #Create browser instance
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False,
            slow_mo=300
        )
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def context(browser):
    #create broswer
    context = await browser.new_context()
    yield context
    await context.close()


@pytest.fixture(scope="function")
async def page(context):
    page = await context.new_page()
    yield page
    await page.close()


@pytest.fixture(scope="function")
async def logged_in_page(page):
    await login_user(page)
    return page


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)