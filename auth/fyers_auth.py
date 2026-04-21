from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
import os

# OPTIONAL: for auto copy
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except:
    CLIPBOARD_AVAILABLE = False


# =========================
# LOAD ENV
# =========================
load_dotenv()

CLIENT_ID = os.getenv("FYERS_CLIENT_ID")
SECRET_KEY = os.getenv("FYERS_SECRET_KEY")
REDIRECT_URI = os.getenv("FYERS_REDIRECT_URI")


# =========================
# GENERATE AUTH URL
# =========================
def generate_auth_url():
    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

    auth_url = session.generate_authcode()

    print("\n" + "="*60)
    print("🔗 OPEN THIS URL IN BROWSER")
    print("="*60)
    print(auth_url)
    print("="*60)
    print("\nAfter login, copy 'auth_code' from redirected URL.\n")


# =========================
# GENERATE ACCESS TOKEN
# =========================
def generate_token(auth_code: str):
    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

    session.set_token(auth_code)
    response = session.generate_token()

    if response.get("s") != "ok":
        raise Exception(f"❌ Token generation failed: {response}")

    access_token = response["access_token"]
    refresh_token = response["refresh_token"]

    # PRINT ACCESS TOKEN CLEARLY
    print("\n" + "="*60)
    print("🎯 ACCESS TOKEN (COPY THIS)")
    print("="*60)
    print(access_token)
    print("="*60)

    # PRINT REFRESH TOKEN
    print("\n🔄 REFRESH TOKEN:\n")
    print(refresh_token)
    print("="*60 + "\n")

    # COPY TO CLIPBOARD (if available)
    if CLIPBOARD_AVAILABLE:
        pyperclip.copy(access_token)
        print("📋 Access token copied to clipboard!")

    return access_token, refresh_token


# =========================
# SAVE TOKEN TO .ENV
# =========================
def save_token_to_env(access_token: str):
    env_path = ".env"

    if not os.path.exists(env_path):
        print("⚠️ .env file not found")
        return

    lines = []
    with open(env_path, "r") as f:
        lines = f.readlines()

    updated = False

    with open(env_path, "w") as f:
        for line in lines:
            if line.startswith("FYERS_ACCESS_TOKEN"):
                f.write(f"FYERS_ACCESS_TOKEN={access_token}\n")
                updated = True
            else:
                f.write(line)

        if not updated:
            f.write(f"\nFYERS_ACCESS_TOKEN={access_token}\n")

    print("💾 Access token saved to .env")


# =========================
# MAIN MENU
# =========================
if __name__ == "__main__":
    print("\n=== FYERS AUTH TOOL ===")
    print("1️⃣ Generate Auth URL")
    print("2️⃣ Generate Access Token")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        generate_auth_url()

    elif choice == "2":
        auth_code = input("\nPaste auth_code: ").strip()
        access_token, _ = generate_token(auth_code)

        save = input("\nSave token to .env? (y/n): ").lower()
        if save == "y":
            save_token_to_env(access_token)

    else:
        print("❌ Invalid choice")