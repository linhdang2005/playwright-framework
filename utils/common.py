import os
import json
import sys
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from utils import config
from pages.login_page import LoginPage



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
def read_config(config=current_dir + "../test_data/config_test_users.json"):
    with open(config, "r") as json_file:
        config_data = json.load(json_file)
    return config_data

# define parame for login function
test_config = current_wd + "/test_data/config_test_users.json"
config_data = read_config(test_config)
test_data = config_data["admin_user"]

# login by normal user
async def login_user(page, email: str = None, password: str = None):
    # test_data is already the admin_user object, not an array
    email = test_data["email"] if email is None else email
    password = test_data["password"] if password is None else password
    try:
        login_page = LoginPage(page)
        url_login = config.CONFIG["url"]
        await page.goto(url_login)  # Use page.goto, not login_page.goto
        await page.wait_for_selector(
            "//button[.='Login']", timeout=10000
        )
        await login_page.login_as(email, password)
        print("Login successfully")
        
    except Exception as e:
        print("Login failed")
        assert False