class Trade:

    def __init__(self,date,action,price,quantity):
        self.date = date
        self.action = action
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "date":self.date,
            "action":self.action,
            "price":self.price,
            "quantity":self.quantity
        }
    