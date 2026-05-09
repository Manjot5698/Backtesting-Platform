# Stock Backtesting Tool - Streamlit App

A modern, professional stock backtesting application built with Streamlit, featuring traditional trading strategies and ML-powered signal generation.

## Features

### Trading Modes
- **Traditional Strategy Mode**: Test pre-built strategies (Moving Average Crossover, RSI, Bollinger Bands)
- **ML Pipeline Mode**: AI-powered trading signals with 15+ technical indicators

### Dashboard Metrics
- Portfolio value tracking
- Total return percentage
- Maximum drawdown analysis
- Sharpe ratio calculation
- Win rate metrics
- ML model performance (Accuracy, Precision, Recall, F1-Score)

### User Interface
- Modern gradient theme with smooth animations
- Responsive card-based layout
- Interactive charts and data tables
- Professional typography
- Mobile-friendly design

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Git (for cloud deployment)
- FYERS API credentials (optional, for live data)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Backtesting-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

## First Backtest

### Traditional Strategy (Easiest)

1. **Load data** 
   - Default ticker: RELIANCE
   - Click "Load Data"
   - Wait for success message

2. **Select strategy**
   - Default: Moving Average
   - Try RSI or Bollinger Bands

3. **Run backtest**
   - Click "Run Backtest"
   - View results instantly

### Expected Results
You should see:
- 4 metric cards (Return, Drawdown, Sharpe, Win Rate)
- Portfolio value chart
- Trade history table
- Latest data points

### ML Mode (Advanced)

1. **Switch to ML Pipeline**
   - Radio button: Select "ML Pipeline"

2. **Load data**
   - Same as Traditional Strategy

3. **Run backtest**
   - Click "Run Backtest"
   - Model trains automatically
   - Generates trading signals

### Expected Results
- 4 ML metrics (Accuracy, Precision, Recall, F1)
- Buy/Sell/Hold signal counts
- Portfolio value chart
- Price with signal overlays
- Signal distribution bar chart
- Predictions with confidence scores

## Mobile Access

### Local Network
Access from mobile on same network:
- Replace `localhost` with your computer's IP
- Example: `http://192.168.1.100:8501`

### Cloud (Streamlit Cloud)
- Access from anywhere
- No server needed
- See "Cloud Deployment" section

## Cloud Deployment (Streamlit Cloud)

### Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repo
   - Select `Backtesting-tool` as the main repo
   - Set main file to `app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to App settings → Secrets
   - Add your FYERS API credentials:
   ```toml
   [fyers]
   API_KEY = "your_fyers_api_key"
   ACCESS_TOKEN = "your_fyers_access_token"
   ```

## How to Use

### Step 1: Configure Settings
- Select stock ticker (e.g., RELIANCE)
- Choose trading mode (Traditional or ML)
- Set quantity for trades

### Step 2: Load Data
- Click "Load Data" button
- Data loads from local cache or FYERS API
- First load may take a few seconds

### Step 3: Run Backtest
- Click "Run Backtest" button
- Review performance metrics
- Analyze charts and trade details

## Project Structure

```
Backtesting-tool/
├── app.py                    # Main Streamlit application
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
├── analytics/
│   └── performance_metrics.py # Performance calculation
├── auth/
│   └── fyers_auth.py        # Authentication logic
├── config/
│   └── settings.py          # Configuration settings
├── data/
│   ├── providers/           # Data source providers
│   ├── raw/                 # Raw data files
│   ├── storage/             # Data storage/loading
│   └── utils/               # Data utilities
├── engine/
│   ├── backtest_engine.py   # Core backtesting engine
│   ├── portfolio.py         # Portfolio tracking
│   └── trade.py             # Trade representation
├── ml/
│   ├── features.py          # Feature engineering
│   ├── model.py             # ML model implementation
│   └── pipeline.py          # ML pipeline
└── strategies/
    ├── base_strategy.py     # Base strategy class
    ├── moving_average.py    # MA strategy
    ├── rsi_strategy.py      # RSI strategy
    ├── Bollinger_strategy.py # Bollinger Bands strategy
    └── strategy_registry.py # Strategy registry
```

## Troubleshooting

### "No data returned"
```
Solution:
1. Check ticker spelling
2. Verify internet connection
3. FYERS service might be down
```

### Missing Dependencies
If you get import errors, reinstall requirements:
```bash
pip install --upgrade -r requirements.txt
```

## Development

### Running Tests
```bash
python -m pytest
```

### Code Structure
- Modular architecture with separate concerns
- Strategy pattern for trading strategies
- ML pipeline for advanced signal generation
- RESTful data providers

## License

See LICENSE file for details.

## Support

For issues or questions, please refer to the project documentation or create an issue on GitHub.
