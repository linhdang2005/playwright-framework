import os, sys
import requests

#read test data
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from utils import common

config_data = common.read_config(
    os.path.join(PROJECT_ROOT, "test_data", "config_test_data.json")
)
test_data_book= config_data["book"]
test_data_user= config_data["user"]
test_data_url= config_data["url"]


def generate_token():
    
    # Define data test
    username = test_data_user["username"]
    password = test_data_user["password"]
    user_id = test_data_user["user_id"]
    generate_token_url = test_data_url["generate_token_url"]
    add_book_url = test_data_url["add_book_url"]

    #Generate token
    generate_token_body = {
        "userName": username,
        "password": password
    }
    token_response = requests.post(
        url=test_data_url["generate_token_url"],
        data=generate_token_body
    )

    # Verify token is generated successfully
    assert token_response.status_code  == 200, token_response.text
    token = token_response.json()["token"]
    print("TOKEN:", token)
    return token