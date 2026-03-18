from engine.portfolio import Portfolio
from engine.trade import Trade


class BacktestEngine:

    def __init__(self, data, quantity=10, initial_capital=100000):

        self.data = data
        self.quantity = quantity
        self.portfolio = Portfolio(initial_capital)

        self.trades = []
        self.open_trades = []

    def run(self):

        portfolio_values = []

        # Remove lookahead bias
        self.data["signal"] = self.data["signal"].shift(1)

        for _, row in self.data.iterrows():

            date = row["Date"]
            price = row["Close"]
            signal = row["signal"]

            # BUY
            if signal == 1:

                if self.portfolio.cash >= price * self.quantity:

                    self.portfolio.buy(price, self.quantity)

                    trade = Trade(date, price, self.quantity)
                    self.open_trades.append(trade)

            # SELL
            elif signal == -1:

                if self.open_trades:

                    trade = self.open_trades.pop(0)  # FIFO

                    self.portfolio.sell(price, trade.quantity)

                    trade.close(date, price)

                    self.trades.append(trade)

            self.portfolio.update_value(price)
            portfolio_values.append(self.portfolio.portfolio_value)

        self.data["portfolio_value"] = portfolio_values

        return self.data