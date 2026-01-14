import os
import json
import sys
import asyncio
from playwright.async_api import expect
from playwright.async_api import async_playwright
from utils import config

success = 0
failure = 1
current_dir = os.getcwd()
current_wd = os.getcwd()
sys.path.append(current_wd)


# Exit program with given exit code
def exit_program(exit_code=success):
    if exit_code == success:
        print("Test finished! Exit the program.")
    sys.exit(exit_code)
# Read configuration
def read_config(config=current_dir + "../test_data/config_test_data.json"):
    with open(config, encoding="utf-8") as json_file:
        config_data = json.load(json_file)
    return config_data

# define parame for login function
test_config = current_wd + "/test_data/config_test_data.json"
config_data = read_config(test_config)
test_data = config_data["user"]

# login by  user
async def login_user(page):
    try:
        url_login = config.CONFIG["url"]
        await page.goto(url_login)  # Use page.goto, not login_page.goto
        await page.wait_for_selector(
            "//button[.='Login']", timeout=10000
        )
        await page.get_by_role("button", name="Login").click()
        await page.wait_for_load_state("load")
        await page.locator("#userName").fill(test_data["username"])
        await page.locator("#password").fill(test_data["password"])
        await page.get_by_role("button", name="Login").click()
        #verify login successfully
        expect(page.locator("label")).to_have_text(test_data["username"])
        print("Login successfully")

    except Exception as e:
        print("Login failed", e)
        assert False