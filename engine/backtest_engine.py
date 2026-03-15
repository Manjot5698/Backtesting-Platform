from engine.trade import Portfolio
from engine.data import Trade

class BacktestEngine:

    def __init__(self,data,quantity =10,initial_capital = 100000):
        self.data = data
        self.quantity = quantity
        self.portfolio = Portfolio(initial_capital)
        self.trades =[]

    def run(self):

        portfolio_values = []
        for _,row in self.data.iterrows():

            date =row["Date"]
            price =row["Close"]
            signal =row["signal"]

            if signal ==1:
                self.portfolio.buy(price,self.quantity)

                self.trades.append(
                    Trade(date,"BUY",price,self.quantity)
                )
            elif signal == -1:

                self.portfolio.sell(price,self.quantity)

                self.trades.append(
                    Trade(date,"SELL",price,self.quantity)
                )
            self.portfolio.update_value(price)

            portfolio_values.append(self.portfolio.value)
        self.data["portfolio_value"] =portfolio_values

        return self.data
    