import pytest_asyncio
from playwright.async_api import async_playwright
import pytest, asyncio
import utils.common as login_user
import os, sys

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=300
        )
        yield browser
        await browser.close()


@pytest_asyncio.fixture(scope="function")
async def context(browser):
    print("👉 DEBUG: entering context fixture")
    context = await browser.new_context()
    yield context
    await context.close()


@pytest_asyncio.fixture(scope="function")
async def page(context):
    page = await context.new_page()
    await login_user.login_user(page)
    yield page
    await page.close()


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)