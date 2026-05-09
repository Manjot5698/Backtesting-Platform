# Deployment Guide

**Your Stock Backtesting Tool is ready for production! 🚀**

## Quick Start (3 Steps)

```bash
# 1. Push to GitHub
git add .
git commit -m "Deployment ready"
git push origin main

# 2. Deploy on Streamlit Cloud
# Go to https://share.streamlit.io
# Click "New app" → select repo → main branch → app.py

# 3. Add Secrets
# In app settings > Secrets, paste your FYERS credentials
# App redeploys automatically
```

**Done! Your live app is ready 🎉**

---

## Pre-Deployment Checklist

- [ ] Generate FYERS credentials: `python auth/fyers_auth.py`
- [ ] Test locally: `streamlit run app.py`
- [ ] All features working locally
- [ ] Repository pushed to GitHub
- [ ] Ready to deploy on Streamlit Cloud

---

## Full Deployment Guide (Streamlit Cloud)

### Prerequisites
- GitHub account with repository
- Streamlit Cloud account (free at https://share.streamlit.io)
- FYERS API credentials

### Step 1: Prepare Repository

```bash
# Ensure everything is committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Visit https://share.streamlit.io
2. Click "New app"
3. Fill in:
   - **Repository**: `username/Backtesting-tool`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click "Deploy"

The app will start deploying. You'll see logs in real-time.

### Step 3: Configure Secrets

1. After deployment completes, click the gear icon (⚙️) in top right
2. Go to "Secrets" tab
3. Paste your credentials:

```
FYERS_CLIENT_ID = "your_client_id"
FYERS_SECRET_KEY = "your_secret_key"
FYERS_REDIRECT_URI = "http://localhost:8501"
FYERS_ACCESS_TOKEN = "your_access_token"
```

4. Click "Save"
5. App will redeploy automatically

### Step 4: Test Your Deployment

- Visit your app URL (shown in deployment logs)
- Test loading data
- Run a backtest
- Share the URL!

---

## Getting FYERS Credentials

### 1. Register on FYERS

1. Go to https://trade.fyers.in
2. Sign up / Log in
3. Go to Dashboard > Settings > API

### 2. Create API Application

- App Name: "Backtesting Tool"
- Redirect URL: `http://localhost:8501` (for local) or your app URL (for cloud)
- Save client ID and secret

### 3. Generate Access Token

```bash
python auth/fyers_auth.py
```

This will:
- Open browser for authentication
- Ask you to authorize the app
- Display your access token
- Copy this token for secrets

### 4. Keep Credentials Safe

⚠️ **Never commit credentials to GitHub**

- ✅ Store in `.env` (local development)
- ✅ Store in Streamlit Secrets (cloud)
- ✅ Use environment variables
- ❌ Don't hardcode in files
- ❌ Don't commit `.env` or `.streamlit/secrets.toml`

---

## Local Development Setup

### Automatic Setup (Windows)

```bash
./setup.bat
```

This will:
1. Create virtual environment
2. Install dependencies
3. Set up .env and .streamlit/secrets.toml
4. Guide you to add credentials

### Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy secrets template
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# Edit with your credentials (use Notepad or VS Code)
# Then run:
streamlit run app.py
```

The app opens at: `http://localhost:8501`

---

## Troubleshooting

### "Missing FYERS credentials" on Cloud

**Problem**: Credentials error when accessing app on Streamlit Cloud

**Solutions**:
1. Go to app Settings > Secrets
2. Verify all 4 credentials are present:
   - `FYERS_CLIENT_ID`
   - `FYERS_SECRET_KEY`
   - `FYERS_REDIRECT_URI`
   - `FYERS_ACCESS_TOKEN`
3. Click "Save"
4. Wait for redeployment
5. Refresh app in browser

### "No data returned" / API errors

**Problem**: Can't fetch stock data on cloud

**Solutions**:
- Verify internet connection works
- Check FYERS service status
- Verify access token is current (may expire)
- Try different stock ticker
- Check data period/interval settings

**Regenerate token**:
```bash
python auth/fyers_auth.py
# Update in Streamlit Secrets
```

### App runs locally but fails on cloud

**Problem**: Works on your computer but not on Streamlit Cloud

**Common causes**:
- Different Python version (use `runtime.txt`)
- Missing system dependencies
- Incorrect environment variable names
- Path issues with file access

**Debug**:
1. Check app logs in Streamlit Cloud dashboard
2. Verify Python version: `python --version`
3. Test locally after any changes

### Slow performance on cloud

**Problem**: App is slow or times out

**Solutions**:
- Reduce data period (e.g., use 1mo instead of 1y)
- Use larger intervals (e.g., 1h instead of 5m)
- Cache results using `@st.cache_data`
- Limit number of backtests per session

---

## Advanced Deployment

### Custom Domain

1. In Streamlit Cloud settings
2. Add custom domain (requires DNS setup)
3. Follow Streamlit's custom domain guide

### Environment Variables

For production settings, add to Streamlit Secrets:

```
# Optional: Custom settings
BACKTEST_TIMEOUT = "300"
MAX_DATA_POINTS = "50000"
DEBUG_MODE = "false"
```

Access in code:
```python
from config.secrets_manager import get_secret
timeout = get_secret("BACKTEST_TIMEOUT", "300")
```

### CI/CD Integration

Set up automatic deployment on GitHub push:

1. Streamlit Cloud auto-deploys on `main` branch
2. For manual control, use GitHub Actions
3. Set deploy secrets as environment variables

---

## Maintenance

### Update Dependencies

```bash
# Update locally
pip install --upgrade -r requirements.txt

# Test thoroughly
streamlit run app.py

# Commit changes
git add requirements.txt
git commit -m "Update dependencies"
git push origin main

# Cloud auto-redeploys
```

### Monitor Performance

- Check Streamlit Cloud dashboard for errors
- Review app analytics
- Monitor data fetch times
- Track user sessions

### Backup Credentials

- Store FYERS credentials in password manager
- Keep backup of access token (generate new if lost)
- Document setup process for team

---

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/deploy/streamlit-cloud
- **FYERS API Docs**: https://api.fyers.in/api-doc/
- **GitHub Issues**: Create issue in repository

