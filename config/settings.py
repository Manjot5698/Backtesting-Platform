import os
from dotenv import load_dotenv

load_dotenv()

FYERS_CLIENT_ID = os.getenv("FYERS_CLIENT_ID")
FYERS_SECRET_KEY = os.getenv("FYERS_SECRET_KEY")
FYERS_ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")

DATA_DIR = "data/raw"