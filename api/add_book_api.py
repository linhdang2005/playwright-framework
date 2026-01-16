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


def add_books(token):
    
    # Define data test
    add_book_url = test_data_url["add_book_url"]
    user_id = test_data_user["user_id"]
    book1_isbn = test_data_book["book1_isbn"]
    book2_isbn = test_data_book["book2_isbn"]

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
    return add_book_response.json()