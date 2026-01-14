import os
from dotenv import load_dotenv


load_dotenv()

CONFIG = {"browser": os.getenv("BROWSER"), "url": os.getenv("URL")}
