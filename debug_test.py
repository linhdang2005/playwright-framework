#!/usr/bin/env python
"""
Debug script to test if browser opens correctly
"""
import asyncio
from playwright.async_api import async_playwright

async def test_browser():
    print("Starting browser test...")
    async with async_playwright() as p:
        print("Launching browser with headless=False...")
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        print("Browser launched!")
        page = await browser.new_page()
        print("New page created!")
        await page.goto("https://www.google.com")
        print("Navigated to Google")
        await asyncio.sleep(5)  # Keep browser open for 5 seconds
        await browser.close()
        print("Browser closed!")

if __name__ == "__main__":
    asyncio.run(test_browser())