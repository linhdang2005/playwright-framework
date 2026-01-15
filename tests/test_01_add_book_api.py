import pytest
import os, sys
import requests
from playwright.sync_api import Playwright

#read test data
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from utils import common

config_data = common.read_config(
    os.path.join(PROJECT_ROOT, "test_data", "config_test_data.json")
)
test_data_book= config_data["book"]
test_data_user= config_data["user"]


def test_add_book_by_api():
    
    # Define data test
    username = test_data_user["username"]
    password = test_data_user["password"]
    user_id = test_data_user["user_id"]
    book1_isbn = test_data_book["book1_isbn"]
    book2_isbn = test_data_book["book2_isbn"]

    #Generate token
    generate_token_url = "https://demoqa.com/Account/v1/GenerateToken"
    generate_token_body = {
        "userName": username,
        "password": password
    }
    token_response = requests.post(
        url=generate_token_url,
        data=generate_token_body
    )

    # Verify token is generated successfully
    assert token_response.status_code  == 200, token_response.text
    token = token_response.json()["token"]
    print("TOKEN:", token)

    # Add book to profile
    add_book_url = "https://demoqa.com/BookStore/v1/Books"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    add_book_body = {
        "userId": user_id,
        "collectionOfIsbns": [
            {
                "isbn": book1_isbn
            },
            {
                "isbn": book2_isbn
            }
        ]
    }

    add_book_response = requests.post(
        url=add_book_url,
        headers=headers,
        json=add_book_body
    )

    assert add_book_response.status_code == 201, add_book_response.text

    print("ADD BOOK RESPONSE:", add_book_response.json())