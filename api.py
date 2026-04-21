from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data.storage.data_loader import DataLoader
from engine.backtest_engine import BacktestEngine
from strategies.strategy_registry import get_strategy

app = FastAPI(title="Backtesting API 🚀")

# ✅ CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📦 REQUEST MODEL
# =========================
class BacktestRequest(BaseModel):
    symbol: str
    strategy_name: str


# ---------------------------
# 🏠 Home Route
# ---------------------------
@app.get("/")
def home():
    return {"status": "Backend running 🚀"}


# ---------------------------
# 📊 Load Data
# ---------------------------
@app.get("/load-data/{symbol}")
def load_stock(symbol: str):
    try:
        data = DataLoader.load_data(symbol)

        return {
            "symbol": symbol,
            "rows": len(data),
            "columns": list(data.columns)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# ⚡ Run Backtest (FIXED)
# ---------------------------
@app.post("/run-backtest")
def run_backtest(request: BacktestRequest):
    try:
        print("🔥 Running backtest...")

        # ✅ GET DATA FROM FRONTEND
        symbol = request.symbol
        strategy_name = request.strategy_name

        print("📌 Selected Strategy:", strategy_name)

        # ✅ LOAD DATA
        data = DataLoader.load_data(symbol)
        print("✅ Data loaded:", data.head())

        # ✅ GET STRATEGY
        strategy_class = get_strategy(strategy_name)
        strategy = strategy_class()
        print("✅ Strategy:", strategy)

        # ✅ RUN ENGINE
        engine = BacktestEngine(data, strategy)
        result = engine.run()
        print("✅ Result:", result)

        # ✅ RESPONSE
        return {
            "symbol": symbol,
            "strategy": strategy_name,
            "total_return": result.total_return,
            "final_balance": result.final_balance,
            "trades": result.trades
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# 📈 Get Available Strategies
# ---------------------------
@app.get("/strategies")
def get_strategies():
    return {
        "available_strategies": [
            "moving_average",
            "rsi",
            "bollinger"
        ]
    }