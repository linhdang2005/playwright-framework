import pytest_asyncio
from playwright.async_api import async_playwright
import pytest, asyncio
import utils.common as login_user
import os, sys



@pytest_asyncio.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(scope="function")
async def page(browser):
    page = await browser.new_page(viewport={"width": 1920, "height": 1080})
    await login_user.login_user(page)
    yield page
    await page.close()

#screenshot on failure
@pytest.hookimpl(trylast=True)
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"reports/screenshots/{item.name}.png"
            asyncio.get_event_loop().run_until_complete(
                page.screenshot(path=screenshot_path, full_page=True)
            )
            print(f"📸 Screenshot saved: {screenshot_path}")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)