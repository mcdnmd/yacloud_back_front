import os

from dotenv import load_dotenv

load_dotenv()

PORT = os.environ.get("PORT", 8080)
HOST = os.environ.get("HOST", "0.0.0.0")
DB_ENDPOINT = os.environ.get("DB_ENDPOINT", "")
DB_PATH = os.environ.get("DB_PATH", "")

