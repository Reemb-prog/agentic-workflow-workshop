import gradio as gr
from accounts import Account, get_share_price

account = Account(10000)

def create_account(initial_deposit):
    global account
    account = Account(initial_deposit)
    return "Account created with initial deposit of {}".format(initial_deposit)

def deposit(amount):
    try:
        account.deposit(amount)
        return "Deposit successful. Current balance: {}".format(account.get_balance())
    except Exception as e:
        return str(e)

def withdraw(amount):
    try:
        account.withdraw(amount)
        return "Withdrawal successful. Current balance: {}".format(account.get_balance())
    except Exception as e:
        return str(e)

def buy(symbol, quantity):
    try:
        account.buy(symbol, quantity)
        return "Buy successful. Current holdings: {}".format(account.get_holdings())
    except Exception as e:
        return str(e)

def sell(symbol, quantity):
    try:
        account.sell(symbol, quantity)
        return "Sell successful. Current holdings: {}".format(account.get_holdings())
    except Exception as e:
        return str(e)

def get_balance():
    return "Current balance: {}".format(account.get_balance())

def get_holdings():
    return "Current holdings: {}".format(account.get_holdings())

def get_transactions():
    return "Current transactions: {}".format(account.get_transactions())

def calculate_portfolio_value():
    return "Current portfolio value: {}".format(account.calculate_portfolio_value())

def calculate_profit_loss():
    return "Current profit/loss: {}".format(account.calculate_profit_loss())

demo = gr.TabbedInterface([
    gr.Interface(create_account, "number", "text", title="Create Account"),
    gr.Interface(deposit, "number", "text", title="Deposit"),
    gr.Interface(withdraw, "number", "text", title="Withdraw"),
    gr.Interface(buy, ["text", "number"], "text", title="Buy"),
    gr.Interface(sell, ["text", "number"], "text", title="Sell"),
    gr.Interface(get_balance, None, "text", title="Get Balance"),
    gr.Interface(get_holdings, None, "text", title="Get Holdings"),
    gr.Interface(get_transactions, None, "text", title="Get Transactions"),
    gr.Interface(calculate_portfolio_value, None, "text", title="Calculate Portfolio Value"),
    gr.Interface(calculate_profit_loss, None, "text", title="Calculate Profit/Loss"),
], tab_names=["Create Account", "Deposit", "Withdraw", "Buy", "Sell", "Get Balance", "Get Holdings", "Get Transactions", "Calculate Portfolio Value", "Calculate Profit/Loss"])

demo.launch()