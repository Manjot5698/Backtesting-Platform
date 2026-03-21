class Trade:

    def __init__(self, entry_date, entry_price, quantity):

        self.entry_date = entry_date
        self.entry_price = entry_price
        self.exit_date = None
        self.exit_price = None
        self.quantity = quantity
        self.pnl = 0

    def close(self, exit_date, exit_price):

        self.exit_date = exit_date
        self.exit_price = exit_price

        self.pnl = (exit_price - self.entry_price) * self.quantity

        self.return_pct = (exit_price / self.entry_price) - 1
        self.holding_days = (exit_date - self.entry_date).days

    def to_dict(self):

        return {
            "entry_date": self.entry_date,
            "entry_price": self.entry_price,
            "exit_date": self.exit_date,
            "exit_price": self.exit_price,
            "quantity": self.quantity,
            "pnl": self.pnl,
            "return_pct": self.return_pct,
            "holding_days": self.holding_days
        }