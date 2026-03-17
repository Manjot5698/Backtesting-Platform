import numpy as np


class PerformanceMetrics:

    @staticmethod
    def total_return(data):
        start = data["portfolio_value"].iloc[0]
        end = data["portfolio_value"].iloc[-1]

        return (end - start) / start

    @staticmethod
    def max_drawdown(data):
        cumulative_max = data["portfolio_value"].cummax()
        drawdown = (data["portfolio_value"] - cumulative_max) / cumulative_max

        return drawdown.min()

    @staticmethod
    def sharpe_ratio(data):
        returns = data["portfolio_value"].pct_change().dropna()

        if returns.std() == 0:
            return 0

        return np.sqrt(252) * (returns.mean() / returns.std())

    @staticmethod
    def volatility(data):
        returns = data["portfolio_value"].pct_change().dropna()

        return returns.std() * (252 ** 0.5)

    @staticmethod
    def final_value(data):
        return data["portfolio_value"].iloc[-1]

    # TEMP: keep win_rate disabled until trade PnL exists
    @staticmethod
    def win_rate(trades):
        return "Not implemented yet"