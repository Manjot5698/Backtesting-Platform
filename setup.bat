@echo off
REM Setup script for local development on Windows

echo.
echo 🚀 Backtesting Tool - Setup Script
echo ==================================
echo.

REM Check Python version
python --version
echo ✓ Python version checked
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
) else (
    echo ✓ Virtual environment exists
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .streamlit\secrets.toml.example .env
    echo ⚠️  Update .env with your FYERS credentials
) else (
    echo ✓ .env file exists
)

REM Create .streamlit/secrets.toml for local development
if not exist ".streamlit\secrets.toml" (
    echo 📝 Creating .streamlit/secrets.toml for local development...
    copy .streamlit\secrets.toml.example .streamlit\secrets.toml
    echo ⚠️  Update .streamlit/secrets.toml with your FYERS credentials
) else (
    echo ✓ .streamlit/secrets.toml exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your FYERS credentials
echo 2. Run: streamlit run app.py
echo.
pause
