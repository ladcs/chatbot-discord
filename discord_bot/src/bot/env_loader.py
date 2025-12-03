import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
user_id = os.getenv("USER_ID")
url = os.getenv("URL")
url_test = os.getenv("URL_TEST")