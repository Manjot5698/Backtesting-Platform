import streamlit as st
import pandas as pd

from data.providers.fyers_provider import FyersProvider
from strategies.strategy_registry import STRATEGY_REGISTRY
from engine.backtest_engine import BacktestEngine
from ml.pipeline import MLPipeline
from analytics.performance_metrics import PerformanceMetrics
from data.utils.ticker_map import TICKER_MAP


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Trading Dashboard", layout="wide")

st.title("📊 Trading Strategy Dashboard")
st.markdown("### Backtest strategies with ML & technical indicators")


# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Controls")

# Using Fyers provider only
provider_choice = "fyers"

search_query = st.sidebar.text_input("🔍 Search Company")

filtered = [
    name for name in TICKER_MAP
    if search_query.lower() in name.lower()
] if search_query else list(TICKER_MAP.keys())

selected_company = st.sidebar.selectbox("Select Company", filtered)
ticker = TICKER_MAP[selected_company]

st.sidebar.success(f"{selected_company}")
st.sidebar.info(f"Using: FYERS")

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-01-01"))

mode = st.sidebar.selectbox(
    "Strategy",
    ["ml", "moving_average", "rsi", "bollinger"]
)

quantity = st.sidebar.number_input("Quantity", value=10)

run_button = st.sidebar.button("🚀 Run Backtest")


# =========================
# MAIN EXECUTION
# =========================
if run_button:

    if start_date >= end_date:
        st.error("Start date must be before end date")
        st.stop()

    with st.spinner("Fetching data & running backtest..."):

        # -------------------------
        # PROVIDER SETUP
        # -------------------------
        provider = FyersProvider()

        base_symbol = ticker.replace(".NS", "")
        formatted_ticker = f"NSE:{base_symbol}-EQ"
        
        # Calculate period dynamically based on selected date range
        days_diff = (end_date - start_date).days
        if days_diff <= 365:
            period = "1y"
        elif days_diff <= 730:
            period = "2y"
        elif days_diff <= 1095:
            period = "3y"
        else:
            period = "5y"

        # -------------------------
        # FETCH DATA
        # -------------------------
        try:
            df = provider.get_price_data(formatted_ticker, period=period)

            if df.empty:
                raise ValueError("Empty DataFrame")

        except Exception as e:
            st.error(f"⚠️ Failed to fetch data: {e}")
            st.stop()

        # -------------------------
        # DATE FILTER
        # -------------------------
        df = df[
            (df["Date"] >= pd.to_datetime(start_date)) &
            (df["Date"] <= pd.to_datetime(end_date))
        ]

        if df.empty:
            st.error("No data for selected range")
            st.stop()

        # -------------------------
        # SIGNAL GENERATION
        # -------------------------
        if mode == "ml":
            pipeline = MLPipeline()
            data = pipeline.run(df)
        else:
            strategy = STRATEGY_REGISTRY[mode]()
            data = strategy.generate_signals(df)

        # -------------------------
        # BACKTEST
        # -------------------------
        engine = BacktestEngine(data, quantity=quantity)
        result = engine.run()

    # =========================
    # METRICS
    # =========================
    st.subheader("📊 Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Return", f"{PerformanceMetrics.total_return(result):.2%}")
    col2.metric("Sharpe", f"{PerformanceMetrics.sharpe_ratio(result):.2f}")
    col3.metric("Drawdown", f"{PerformanceMetrics.max_drawdown(result):.2%}")
    col4.metric("Win Rate", f"{PerformanceMetrics.win_rate(engine.trades):.2%}")

    st.divider()

    # =========================
    # PRICE CHART
    # =========================
    st.subheader("📉 Price Chart with Signals")

    chart_df = result.copy()
    chart_df.set_index("Date", inplace=True)

    buy = chart_df[chart_df["signal"] == 1]
    sell = chart_df[chart_df["signal"] == -1]

    st.line_chart(chart_df["Close"])

    st.write("🟢 Buy Signals:", len(buy))
    st.write("🔴 Sell Signals:", len(sell))

    st.divider()

    # =========================
    # PORTFOLIO
    # =========================
    st.subheader("💼 Portfolio Value")

    st.line_chart(chart_df["portfolio_value"])

    st.write(
        f"Initial: {chart_df['portfolio_value'].iloc[0]:.2f} | "
        f"Final: {chart_df['portfolio_value'].iloc[-1]:.2f}"
    )

else:
    st.info("Use the sidebar to configure and run a backtest")