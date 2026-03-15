class Portfolio:

    def __init__(self,initial_capital):
        self.cash = initial_capital
        self.position = 0
        self.portfolio_value = initial_capital

    def buy(self,price,quantity):
        cost = price*quantity
        if self.cash >=cost:
            self.cash -=cost
            self.position +=quantity
    
    def sell(self,price,quantity):

        if self.position >=quantity:
            self.cash += price*quantity
            self.position -=quantity

    def update_value(self,price):

        self.portfolio_value = self.cash + self.position*price