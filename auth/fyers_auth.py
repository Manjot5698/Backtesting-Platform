from fyers_apiv3 import fyersModel
from config.secrets_manager import get_secret

# =========================
# LOAD SECRETS
# =========================
CLIENT_ID = get_secret("FYERS_CLIENT_ID")
SECRET_KEY = get_secret("FYERS_SECRET_KEY")
REDIRECT_URI = get_secret("FYERS_REDIRECT_URI")

# =========================
# VALIDATION
# =========================
if not CLIENT_ID or not SECRET_KEY or not REDIRECT_URI:
    raise ValueError(
        "Missing FYERS credentials. Configure in:\n"
        "- Local: .env file\n"
        "- Streamlit Cloud: Settings > Secrets"
    )

# =========================
# CREATE SESSION
# =========================
session = fyersModel.SessionModel(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type="code",
    grant_type="authorization_code"
)

# =========================
# STEP 1: GENERATE AUTH URL
# =========================
auth_url = session.generate_authcode()

print("\n" + "="*60)
print("🔗 OPEN THIS URL IN YOUR BROWSER")
print("="*60)
print(auth_url)
print("="*60)
print("\n➡ After login, copy 'auth_code' from redirected URL\n")
# =========================
# STEP 2: GENERATE TOKEN
# =========================
auth_code = input("Paste auth_code: ").strip()

session.set_token(auth_code)
response = session.generate_token()

if response.get("s") != "ok":
    raise Exception(f"Token generation failed: {response}")

print("\nACCESS TOKEN:\n")
print(response["access_token"])