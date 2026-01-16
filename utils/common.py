import os
import json
import sys
import asyncio
from playwright.async_api import expect
from utils import config
from pages.login_page import loginpage



#read test data
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Read configuration
def read_config(config=PROJECT_ROOT + "/test_data/config_test_data.json"):
    with open(config, encoding="utf-8") as json_file:
        config_data = json.load(json_file)
    return config_data

# define parame for login function
config_data = read_config(
    os.path.join(PROJECT_ROOT, "test_data", "config_test_data.json")
)
test_data = config_data["user"]

# login by  user
async def login_user(page):
    username = test_data["username"]
    password = test_data["password"]
    url_login = config.CONFIG["url"]
    try:
        login_page = loginpage(page)
        await page.goto(url_login)
        await login_page.login_button.wait_for(timeout=10000)
        await login_page.login_button.click()
        await login_page.username.fill(username)
        await login_page.password.fill(password)
        await login_page.login_button.click()
        #verify login successfully
        await expect(login_page.login_username_display).to_have_text(username)
        print("Login successfully")

    except Exception as e:
        print("Login failed", e)
        assert False

# Exit program with given exit code
success = 0
failure = 1
def exit_program(exit_code=0):
    if exit_code == 0:
        print("Test finished! Exit the program.")
    sys.exit(exit_code)