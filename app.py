import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np

from data.providers.fyers_provider import FyersProvider
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine
from analytics.performance_metrics import PerformanceMetrics
from ml.pipeline import MLPipeline
from ml.features import FeatureEngineer
from config.secrets_manager import get_secret

# =========================
# VALIDATE CREDENTIALS
# =========================
try:
    client_id = get_secret("FYERS_CLIENT_ID")
    access_token = get_secret("FYERS_ACCESS_TOKEN")
    if not client_id or not access_token:
        st.error(
            "❌ Missing FYERS Credentials\n\n"
            "**Local Development:**\n"
            "1. Create `.env` file in project root\n"
            "2. Add: `FYERS_CLIENT_ID`, `FYERS_SECRET_KEY`, `FYERS_REDIRECT_URI`, `FYERS_ACCESS_TOKEN`\n\n"
            "**Streamlit Cloud:**\n"
            "1. Go to App settings > Secrets\n"
            "2. Add the same credentials\n"
            "3. See `.streamlit/secrets.toml.template` for format"
        )
        st.stop()
except Exception as e:
    st.error(f"Configuration Error: {str(e)}")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #0891b2 0%, #0284c7 100%);
        color: #333;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #0891b2 0%, #0284c7 100%);
        padding: 40px 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .header-container h1 {
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
    }
    
    .header-container p {
        font-size: 1em;
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    .sidebar-title {
        font-size: 1.3em;
        font-weight: 600;
        color: #0891b2;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #0891b2;
        padding-bottom: 10px;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #0891b2;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: #0891b2;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #666;
        font-weight: 500;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #0891b2 0%, #0284c7 100%);
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(8, 145, 178, 0.4);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5em;
        font-weight: 700;
        color: #0891b2;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #0891b2;
    }
    
    /* Charts Container */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
    }
    
    /* Data Table Styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Radio Button Styling */
    .stRadio > label {
        font-weight: 500;
        color: #333;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-radius: 8px;
    }
    
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 8px;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-radius: 8px;
    }
    
    /* Divider */
    .divider {
        border-top: 2px solid #0891b2;
        margin: 30px 0;
    }
    
    </style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="Backtesting Tool", layout="wide", initial_sidebar_state="expanded")

# Header
st.markdown("""
    <div class="header-container">
        <h1>Stock Backtesting Tool</h1>
        <p>Advanced trading strategy backtesting with ML-powered signal generation</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.markdown('<div class="sidebar-title">Configuration</div>', unsafe_allow_html=True)

ticker = st.sidebar.text_input("Stock Ticker", value="RELIANCE", placeholder="e.g., RELIANCE")


# Mode selection: Traditional Strategy or ML Pipeline
mode_type = st.sidebar.radio(
    "Select Mode",
    options=["Traditional Strategy", "ML Pipeline"],
    index=0
)

if mode_type == "Traditional Strategy":
    strategy_mode = st.sidebar.selectbox(
        "Select Strategy",
        options=list(STRATEGY_REGISTRY.keys()),
        index=0
    )
else:
    strategy_mode = None

quantity = st.sidebar.number_input("Quantity", min_value=1, value=10, step=1)

# Time Period Selection
st.sidebar.markdown('<div class="sidebar-title">Time Period</div>', unsafe_allow_html=True)

period = st.sidebar.selectbox(
    "Select Period",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y"],
    index=1,
    help="Time period for historical data"
)

interval = st.sidebar.selectbox(
    "Select Interval",
    options=["1m", "5m", "15m", "30m", "1h", "1d"],
    index=1,
    help="Candle interval (bar size)"
)

# Load data
st.sidebar.markdown('<div class="sidebar-title">Data Management</div>', unsafe_allow_html=True)
if st.sidebar.button("Load Data", use_container_width=True):
    try:
        st.sidebar.info(f"Fetching {ticker} from FYERS ({period} | {interval})...")
        provider = FyersProvider()
        df = provider.get_price_data(ticker, period=period, interval=interval)
        
        if df.empty:
            st.sidebar.error(f"No data returned for {ticker}")
            st.stop()
        
        st.sidebar.success(f"{ticker} - data loaded successfully ({len(df)} candles)")
        st.session_state.df = df
        st.session_state.ticker = ticker
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")
        st.stop()

# Run backtest
st.sidebar.markdown('<div class="sidebar-title">Execute</div>', unsafe_allow_html=True)
if st.sidebar.button("Run Backtest", use_container_width=True):
    if "df" not in st.session_state:
        st.error("Please load data first")
        st.stop()
    
    df = st.session_state.df
    
    try:
        if mode_type == "Traditional Strategy":
            # Traditional strategy backtesting
            strategy_class = STRATEGY_REGISTRY[strategy_mode]
            strategy = strategy_class()
            
            engine = BacktestEngine(df, strategy=strategy, quantity=quantity)
            result = engine.run()
            
            st.session_state.result = result
            st.session_state.engine = engine
            st.session_state.ml_metrics = None
            
            st.success("Backtest completed!")
        
        else:  # ML Pipeline mode
            st.info("Running ML Pipeline...")
            
            # Run ML pipeline
            ml_pipeline = MLPipeline()
            ml_result = ml_pipeline.run(df)
            
            # Store ML metrics
            ml_metrics = ml_pipeline.metrics if hasattr(ml_pipeline, 'metrics') else {}
            
            # Convert ML signals to strategy-compatible format
            # Add portfolio value tracking using ML signals
            ml_result_backtest = ml_result.copy()
            ml_result_backtest["portfolio_value"] = 10000  # Starting value
            
            # Simulate trading based on ML signals
            position = 0
            portfolio_value = 10000
            cash = 10000
            holdings = 0
            
            for idx in range(len(ml_result_backtest)):
                signal = ml_result_backtest.iloc[idx]["signal"]
                close_price = ml_result_backtest.iloc[idx]["Close"]
                
                if signal == 1 and position == 0:  # Buy signal
                    holdings = quantity
                    cash -= quantity * close_price
                    position = 1
                elif signal == -1 and position == 1:  # Sell signal
                    cash += holdings * close_price
                    holdings = 0
                    position = 0
                
                portfolio_value = cash + (holdings * close_price)
                ml_result_backtest.loc[idx, "portfolio_value"] = portfolio_value
            
            st.session_state.result = ml_result_backtest
            st.session_state.engine = None
            st.session_state.ml_metrics = ml_metrics
            
            st.success("ML Pipeline & Backtest completed!")
            
    except Exception as e:
        st.error(f"Error running backtest: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

# Display results
if "result" in st.session_state:
    result = st.session_state.result
    engine = st.session_state.get("engine")
    ml_metrics = st.session_state.get("ml_metrics")
    
    st.markdown('<h2 class="section-header">Backtest Results</h2>', unsafe_allow_html=True)
    
    if mode_type == "Traditional Strategy" and engine is not None:
        # Display traditional strategy results
        st.markdown("### Performance Metrics", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_return = PerformanceMetrics.total_return(result)
        max_drawdown = PerformanceMetrics.max_drawdown(result)
        sharpe_ratio = PerformanceMetrics.sharpe_ratio(result)
        win_rate = PerformanceMetrics.win_rate(engine.trades)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Return</div>
                    <div class="metric-value">{total_return:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Max Drawdown</div>
                    <div class="metric-value">{max_drawdown:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Sharpe Ratio</div>
                    <div class="metric-value">{sharpe_ratio:.4f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Win Rate</div>
                    <div class="metric-value">{win_rate:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Portfolio value chart
        st.markdown('<h3 class="section-header">Portfolio Value Over Time</h3>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_data = result[["portfolio_value"]].copy()
        st.line_chart(chart_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Trades
        st.markdown('<h3 class="section-header">Recent Trades</h3>', unsafe_allow_html=True)
        trades_list = [trade.to_dict() for trade in engine.trades[:10]]
        st.dataframe(pd.DataFrame(trades_list), use_container_width=True)
    
    else:  # ML Pipeline mode
        st.markdown("### ML Model Performance", unsafe_allow_html=True)
        
        # Display ML Model Metrics
        if ml_metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Accuracy</div>
                        <div class="metric-value">{ml_metrics.get('accuracy', 0):.4f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Precision</div>
                        <div class="metric-value">{ml_metrics.get('precision', 0):.4f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Recall</div>
                        <div class="metric-value">{ml_metrics.get('recall', 0):.4f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">F1-Score</div>
                        <div class="metric-value">{ml_metrics.get('f1_score', 0):.4f}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Display ML signal distribution
        st.markdown("### Trading Signals", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        signal_counts = result["signal"].value_counts()
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Buy Signals</div>
                    <div class="metric-value">🟢 {int(signal_counts.get(1, 0))}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Sell Signals</div>
                    <div class="metric-value">🔴 {int(signal_counts.get(-1, 0))}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Hold Signals</div>
                    <div class="metric-value">🟡 {int(signal_counts.get(0, 0))}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Portfolio value chart
        st.markdown('<h3 class="section-header">Portfolio Value Over Time (ML Strategy)</h3>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_data = result[["portfolio_value"]].copy()
        st.line_chart(chart_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ML Signals visualization
        st.markdown('<h3 class="section-header">Price with Trading Signals</h3>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        signal_chart = result[["Close", "signal"]].copy()
        st.line_chart(signal_chart["Close"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Signal distribution
        st.markdown('<h3 class="section-header">Signal Distribution</h3>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.bar_chart(signal_counts)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent data with predictions
        st.markdown('<h3 class="section-header">Recent Predictions & Data</h3>', unsafe_allow_html=True)
        display_cols = ["Close", "return", "RSI", "signal", "confidence", "portfolio_value"]
        available_cols = [col for col in display_cols if col in result.columns]
        st.dataframe(result[available_cols].tail(20), use_container_width=True)
    
    # Final data
    st.markdown('<h3 class="section-header">Latest Data Points</h3>', unsafe_allow_html=True)
    st.dataframe(result.tail(10), use_container_width=True)
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; background: white; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #0891b2;">👈 Get Started</h3>
            <p style="color: #666;">1. Select your configuration in the sidebar</p>
            <p style="color: #666;">2. Click "Load Data" to fetch stock data</p>
            <p style="color: #666;">3. Click "Run Backtest" to analyze performance</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="margin-top: 50px; padding: 30px; text-align: center; background: linear-gradient(135deg, #0891b2 0%, #0284c7 100%); color: white; border-radius: 10px;">
        <h4>Stock Backtesting Tool</h4>
        <p style="margin: 10px 0; opacity: 0.9;">Advanced trading strategy analysis with machine learning</p>
        <p style="margin: 10px 0; font-size: 0.9em; opacity: 0.8;">© 2026 | Built with Streamlit | Data powered by Fyers API</p>
    </div>
""", unsafe_allow_html=True)
