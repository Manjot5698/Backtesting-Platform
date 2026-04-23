import pandas as pd
from data.providers.fyers_provider import FyersProvider
from data.providers.yfinance_provider import YFinanceProvider


class LiveDataProvider:

    def __init__(self):
        self.fyers = None
        self.yfinance = YFinanceProvider()

        # Try initializing FYERS safely
        try:
            self.fyers = FyersProvider()
        except Exception as e:
            print("⚠ FYERS init failed:", e)

    def get_data(self, symbol: str) -> pd.DataFrame:

        # =========================
        # TRY FYERS (PRIMARY)
        # =========================
        if self.fyers:
            try:
                print("📡 Using FYERS LIVE data...")
                data = self.fyers.get_price_data(symbol)

                if not data.empty:
                    print("✅ FYERS SUCCESS")
                    return data

            except Exception as e:
                print("❌ FYERS ERROR:", e)

        # =========================
        # FALLBACK YFINANCE
        # =========================
        try:
            print("📡 Using YFINANCE fallback...")
            data = self.yfinance.get_price_data(symbol)

            if data.empty:
                raise ValueError("yfinance returned empty data")

            print("✅ YFINANCE SUCCESS")
            return data

        except Exception as e:
            raise ValueError(f"❌ Both FYERS & YFINANCE failed: {e}")