from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

from data.providers.yfinance_provider import YFinanceProvider
from data.providers.fyers_provider import FyersProvider
from engine.backtest_engine import BacktestEngine
from strategies.strategy_registry import get_strategy

app = FastAPI(title="Backtesting API 🚀")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================
class BacktestRequest(BaseModel):
    symbol: str
    strategy_name: str


# =========================
# 🔥 LIVE DATA FETCH (FYERS + FALLBACK)
# =========================
def get_live_data(symbol: str):

    fyers = None
    try:
        fyers = FyersProvider()
    except Exception as e:
        print("⚠ FYERS init failed:", e)

    yfinance = YFinanceProvider()

    # ---------- TRY FYERS ----------
    if fyers:
        try:
            print("📡 Trying FYERS...")
            data = fyers.get_price_data(symbol)

            if not data.empty:
                print("✅ FYERS SUCCESS")
                return data, "fyers"

        except Exception as e:
            print("❌ FYERS ERROR:", e)

    # ---------- FALLBACK ----------
    print("📡 Using yfinance fallback...")
    data = yfinance.get_price_data(symbol)

    if data.empty:
        raise ValueError("❌ No data received")

    print("✅ YFINANCE SUCCESS")
    return data, "yfinance"


# =========================
# 🧹 DATA CLEANER (CRITICAL FIX)
# =========================
def clean_data(data: pd.DataFrame):

    # FIX multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    required_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]

    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing column: {col}")

    # FORCE 1D
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        data[col] = data[col].squeeze()

    # CONVERT TYPES
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    # CLEAN
    data = data.dropna().reset_index(drop=True)

    if data.empty:
        raise ValueError("❌ Data became empty after cleaning")

    return data


# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"status": "Backend running 🚀"}


# =========================
# LOAD DATA (UI INFO)
# =========================
@app.get("/load-data/{symbol}")
def load_stock(symbol: str):
    try:
        data, source = get_live_data(symbol)

        return {
            "symbol": symbol,
            "rows": len(data),
            "columns": list(data.columns),
            "source": source
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# 🚀 RUN BACKTEST (FINAL FIXED)
# =========================
@app.post("/run-backtest")
def run_backtest(request: BacktestRequest):
    try:
        print("\n🔥 Running backtest...")
        print("📌 Strategy:", request.strategy_name)

        # ---------- FETCH LIVE DATA ----------
        data, source = get_live_data(request.symbol)

        print("📊 Data Source:", source)
        print("📅 Last Candle:", data["Date"].iloc[-1])

        # ---------- CLEAN DATA ----------
        data = clean_data(data)
        print("✅ Data cleaned")

        # ---------- STRATEGY ----------
        strategy_class = get_strategy(request.strategy_name)
        strategy = strategy_class()

        # ---------- ENGINE ----------
        engine = BacktestEngine(data, strategy)
        result_df = engine.run()

        if result_df.empty:
            raise ValueError("No result generated")

        # ---------- METRICS ----------
        initial = result_df["portfolio_value"].iloc[0]
        final = result_df["portfolio_value"].iloc[-1]

        total_return = ((final - initial) / initial) * 100

        # ---------- TRADES ----------
        trades = [
            {
                "entry_price": float(t.entry_price),
                "exit_price": float(t.exit_price),
                "pnl": float(t.pnl),
                "entry_date": str(t.entry_date),
                "exit_date": str(t.exit_date)
            }
            for t in engine.trades
        ] if engine.trades else []

        # ---------- EQUITY CURVE (FOR GRAPH) ----------
        equity_curve = [
            {
                "date": str(row["Date"]),
                "value": float(row["portfolio_value"])
            }
            for _, row in result_df.iterrows()
        ]

        return {
            "symbol": request.symbol,
            "strategy": request.strategy_name,
            "total_return": round(total_return, 2),
            "final_balance": round(final, 2),
            "trades": trades,
            "equity_curve": equity_curve,
            "data_source": source
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# STRATEGIES
# =========================
@app.get("/strategies")
def get_strategies():
    return {
        "available_strategies": [
            "moving_average",
            "rsi",
            "bollinger"
        ]
    }