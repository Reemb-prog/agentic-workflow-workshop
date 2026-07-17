import unittest
from unittest.mock import patch
from accounts import Account, InsufficientFundsError, InsufficientSharesError, UnknownSymbolError, get_share_price
import datetime

class TestAccounts(unittest.TestCase):

    def test_create_account(self):
        account = Account(1000)
        self.assertEqual(account.balance, 1000)
        self.assertEqual(account.holdings, {})
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]['type'], 'deposit')
        self.assertEqual(account.transactions[0]['amount'], 1000)

    def test_deposit(self):
        account = Account(1000)
        account.deposit(500)
        self.assertEqual(account.balance, 1500)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]['type'], 'deposit')
        self.assertEqual(account.transactions[1]['amount'], 500)

    def test_withdraw(self):
        account = Account(1000)
        account.withdraw(500)
        self.assertEqual(account.balance, 500)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]['type'], 'withdrawal')
        self.assertEqual(account.transactions[1]['amount'], 500)

    def test_withdraw_insufficient_funds(self):
        account = Account(1000)
        with self.assertRaises(InsufficientFundsError):
            account.withdraw(1500)

    def test_buy(self):
        account = Account(1000)
        account.buy('AAPL', 5)
        self.assertEqual(account.balance, 1000 - get_share_price('AAPL') * 5)
        self.assertEqual(account.holdings, {'AAPL': 5})
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]['type'], 'buy')
        self.assertEqual(account.transactions[1]['symbol'], 'AAPL')
        self.assertEqual(account.transactions[1]['quantity'], 5)

    def test_buy_insufficient_funds(self):
        account = Account(1000)
        with self.assertRaises(InsufficientFundsError):
            account.buy('AAPL', 1000)

    def test_buy_unknown_symbol(self):
        account = Account(1000)
        with self.assertRaises(UnknownSymbolError):
            account.buy('UNKNOWN', 5)

    def test_sell(self):
        account = Account(1000)
        account.buy('AAPL', 5)
        account.sell('AAPL', 3)
        self.assertEqual(account.balance, 1000 - get_share_price('AAPL') * 5 + get_share_price('AAPL') * 3)
        self.assertEqual(account.holdings, {'AAPL': 2})
        self.assertEqual(len(account.transactions), 3)
        self.assertEqual(account.transactions[2]['type'], 'sell')
        self.assertEqual(account.transactions[2]['symbol'], 'AAPL')
        self.assertEqual(account.transactions[2]['quantity'], 3)

    def test_sell_insufficient_shares(self):
        account = Account(1000)
        account.buy('AAPL', 5)
        with self.assertRaises(InsufficientSharesError):
            account.sell('AAPL', 10)

    def test_sell_unknown_symbol(self):
        account = Account(1000)
        with self.assertRaises(InsufficientSharesError):
            account.sell('AAPL', 5)

    def test_get_balance(self):
        account = Account(1000)
        self.assertEqual(account.get_balance(), 1000)

    def test_get_holdings(self):
        account = Account(1000)
        account.buy('AAPL', 5)
        self.assertEqual(account.get_holdings(), {'AAPL': 5})

    def test_get_transactions(self):
        account = Account(1000)
        account.deposit(500)
        account.buy('AAPL', 5)
        self.assertEqual(len(account.get_transactions()), 3)

    def test_calculate_portfolio_value(self):
        account = Account(1000)
        account.buy('AAPL', 5)
        portfolio_value = account.balance + get_share_price('AAPL') * 5
        self.assertEqual(account.calculate_portfolio_value(), portfolio_value)

    def test_calculate_profit_loss(self):
        account = Account(1000)
        account.buy('AAPL', 5)
        profit_loss = account.calculate_portfolio_value() - 1000
        self.assertEqual(account.calculate_profit_loss(), profit_loss)

if __name__ == '__main__':
    unittest.main()