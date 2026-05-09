from config.secrets_manager import get_secret

FYERS_CLIENT_ID = get_secret("FYERS_CLIENT_ID")
FYERS_SECRET_KEY = get_secret("FYERS_SECRET_KEY")
FYERS_ACCESS_TOKEN = get_secret("FYERS_ACCESS_TOKEN")

DATA_DIR = "data/raw"