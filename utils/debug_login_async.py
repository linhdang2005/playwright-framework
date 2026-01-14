import asyncio
import os
import sys

# add project root vào sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from playwright.async_api import async_playwright
from utils.common import login_user


async def main():
    print("🚀 [DEBUG] Start debug login")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=800
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("🚀 [DEBUG] Browser & page created")

        await login_user(page)

        print("⏸️ [DEBUG] Pause to inspect UI")
        await page.pause()

        await browser.close()
        print("🧹 [DEBUG] Browser closed")


if __name__ == "__main__":
    asyncio.run(main())
