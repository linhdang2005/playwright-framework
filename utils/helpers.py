import os
import json
import random
import string
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_test_data(filename: str) -> Dict[str, Any]:
    """Load test data from JSON file"""
    test_data_path = os.getenv("TEST_DATA_PATH", "./tests/data")
    file_path = os.path.join(test_data_path, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test data file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        return json.load(file)


def generate_random_string(length: int = 8) -> str:
    """Generate a random string of specified length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email() -> str:
    """Generate a random email address"""
    username = generate_random_string(8)
    domain = generate_random_string(6)
    return f"{username}@{domain}.com"


def generate_test_user_data() -> Dict[str, str]:
    """Generate test user data"""
    return {
        "email": generate_random_email(),
        "password": generate_random_string(12),
        "first_name": generate_random_string(6).capitalize(),
        "last_name": generate_random_string(8).capitalize(),
        "phone": f"+1{random.randint(1000000000, 9999999999)}"
    }


def wait_for_file_download(download_path: str, timeout: int = 30) -> bool:
    """Wait for a file to be downloaded"""
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(download_path) and os.path.getsize(download_path) > 0:
            return True
        time.sleep(1)
    return False


def cleanup_downloads(directory: str = None) -> None:
    """Clean up downloaded files"""
    download_dir = directory or os.getenv("DOWNLOADS_PATH", "./tests/downloads")
    
    if os.path.exists(download_dir):
        for filename in os.listdir(download_dir):
            file_path = os.path.join(download_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


def get_browser_config() -> Dict[str, Any]:
    """Get browser configuration from environment"""
    return {
        "browser": os.getenv("BROWSER", "chromium"),
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "slow_mo": int(os.getenv("SLOW_MO", "0")),
        "timeout": int(os.getenv("TIMEOUT", "30000"))
    }