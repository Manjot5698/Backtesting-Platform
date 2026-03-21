from engine.portfolio import Portfolio
from engine.trade import Trade


class BacktestEngine:

    def __init__(self, data, quantity=10, initial_capital=100000, cost_pct=0.001):

        self.data = data.copy()
        self.quantity = quantity
        self.portfolio = Portfolio(initial_capital)

        self.trades = []
        self.open_trades = []

        self.cost_pct = cost_pct

    def run(self):

        portfolio_values = []

        # Remove lookahead bias
        self.data["signal"] = self.data["signal"].shift(1)
        self.data = self.data.dropna(subset=["signal"]).reset_index(drop=True)

        for _, row in self.data.iterrows():

            date = row["Date"]
            price = row["Close"]
            signal = row["signal"]

            # =======================
            # BUY (only if NOT holding)
            # =======================
            if signal == 1 and self.portfolio.position == 0:

                cost = price * self.quantity * (1 + self.cost_pct)

                if self.portfolio.cash >= cost:

                    self.portfolio.buy(price, self.quantity, cost_pct=self.cost_pct)

                    trade = Trade(date, price, self.quantity)
                    self.open_trades.append(trade)

            # =======================
            # SELL (only if holding)
            # =======================
            elif signal == -1 and self.portfolio.position > 0:

                if self.open_trades:  # safety check

                    trade = self.open_trades.pop(0)  # FIFO

                    self.portfolio.sell(price, trade.quantity, cost_pct=self.cost_pct)

                    trade.close(date, price)
                    self.trades.append(trade)

            # =======================
            # UPDATE PORTFOLIO VALUE
            # =======================
            self.portfolio.update_value(price)
            portfolio_values.append(self.portfolio.portfolio_value)

        self.data["portfolio_value"] = portfolio_values

        return self.data