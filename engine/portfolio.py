class Portfolio:

    def __init__(self,initial_capital):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0
        self.portfolio_value = initial_capital

    def buy(self, price, quantity, cost_pct=0.001):
        cost = price * quantity * (1 + cost_pct)
        if self.cash >= cost:
            self.cash -= cost
            self.position += quantity


    def sell(self, price, quantity, cost_pct=0.001):
        proceeds = price * quantity * (1 - cost_pct)
        if self.position >= quantity:
            self.cash += proceeds
            self.position -= quantity

    def update_value(self,price):

        self.portfolio_value = self.cash + self.position*price