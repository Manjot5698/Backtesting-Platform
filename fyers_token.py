from fyers_apiv3.fyersModel import SessionModel
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("FYERS_CLIENT_ID")
secret_key = os.getenv("FYERS_SECRET_KEY")
redirect_uri = os.getenv("FYERS_REDIRECT_URI")

# Step 1: Generate login URL
session = SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code",
    grant_type="authorization_code"
)

auth_url = session.generate_authcode()

print("\nOpen this URL in your browser:\n")
print(auth_url)

# Step 2: Paste auth_code
auth_code = input("\nPaste auth_code here: ").strip()

# Step 3: Generate access token
session.set_token(auth_code)
response = session.generate_token()

if response.get("s") != "ok":
    print("Error:", response)
else:
    print("\nYour ACCESS TOKEN:\n")
    print(response["access_token"])