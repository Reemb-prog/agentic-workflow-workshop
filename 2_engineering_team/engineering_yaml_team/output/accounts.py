import datetime

class InsufficientFundsError(Exception):
    pass

class InsufficientSharesError(Exception):
    pass

class UnknownSymbolError(Exception):
    pass

def get_share_price(symbol):
    prices = {
        'AAPL': 180.00,
        'TSLA': 280.00,
        'GOOGL': 130.00
    }
    if symbol.upper() not in prices:
        raise UnknownSymbolError(f"Unknown symbol: {symbol}")
    return prices[symbol.upper()]

class Account:
    def __init__(self, initial_deposit):
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit
        self.transactions.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'deposit',
            'amount': initial_deposit
        })

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'deposit',
            'amount': amount
        })

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        self.balance -= amount
        self.transactions.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'withdrawal',
            'amount': amount
        })

    def buy(self, symbol, quantity):
        try:
            price = get_share_price(symbol)
        except UnknownSymbolError as e:
            raise UnknownSymbolError(f"Unknown symbol: {symbol}")
        cost = price * quantity
        if cost > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        self.balance -= cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': cost
        })

    def sell(self, symbol, quantity):
        if symbol not in self.holdings:
            raise InsufficientSharesError("You do not own any shares of this stock")
        if quantity > self.holdings[symbol]:
            raise InsufficientSharesError("You do not own enough shares to sell")
        price = get_share_price(symbol)
        proceeds = price * quantity
        self.balance += proceeds
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': proceeds
        })

    def get_balance(self):
        return self.balance

    def get_holdings(self):
        return self.holdings.copy()

    def get_transactions(self):
        return self.transactions.copy()

    def calculate_portfolio_value(self):
        portfolio_value = self.balance
        for symbol, quantity in self.holdings.items():
            portfolio_value += get_share_price(symbol) * quantity
        return portfolio_value

    def calculate_profit_loss(self):
        return self.calculate_portfolio_value() - self.initial_deposit
