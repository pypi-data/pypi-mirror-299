import pandas as pd
from ..feed.PandasPart import PandasPart

class AccountSpot:
    """
    Represents a trading account for managing spot transactions, including buying and selling assets.

    Attributes:
        _code (str): The unique identifier code for the account.
        _name (str): The name associated with the account.
        _fee (float): The transaction fee percentage (e.g., 0.015 for 0.015%).
        _tax (float): The transaction tax percentage (e.g., 0.38 for 0.38%).
        _balance (int): The current cash balance available for trading.
        _account_price (int): The current total value of the account (cash + value of held assets).
        _quantity (int): The total number of asset units currently held.
        _invested (int): The total amount invested in purchasing assets.
        _average_price (int): The average price per asset unit based on investments.
        _history_asset (pd.DataFrame): DataFrame tracking the history of account assets.
        _history_trade (pd.DataFrame): DataFrame tracking the history of trades executed.
    """

    def __init__(self, code, name, balance=1000000, fee=0.015, tax=0.38):
        """
        Initializes a new instance of the SpotAccount class.

        Args:
            code (str): The unique identifier code for the account.
            name (str): The name associated with the account.
            balance (int, optional): The initial cash balance. Defaults to 1,000,000.
            fee (float, optional): The transaction fee percentage. Defaults to 0.015 (1.5%).
            tax (float, optional): The transaction tax percentage. Defaults to 0.38 (38%).
        """
        self._code = code
        self._name = name
        self._fee = fee / 100   # Transaction fee percentage (e.g., 0.015% as 0.00015)
        self._tax = tax / 100   # Transaction tax percentage (e.g., 0.38% as 0.0038)
        
        self._balance = balance        # Current cash balance (initial capital)
        self._account_price = 0        # Current total account value (cash + asset value)
        
        self._quantity = 0             # Total number of asset units held
        self._invested = 0             # Total amount invested in purchasing assets
        self._average_price = 0        # Average price per asset unit
        
        # DataFrame to track the history of account assets
        self._history_asset = pd.DataFrame(columns=[
            "reg_day", "balance", "quantity", "average_price", "invested", "account"
        ])
        
        # DataFrame to track the history of trades executed
        self._history_trade = pd.DataFrame(columns=[
            "reg_day", "action", "price", "quantity", "fee", "tax", "net_price", "rate"
        ])

    def getHistory(self):
        """
        Retrieves the historical records of account assets and trades.

        Returns:
            tuple: A tuple containing two DataFrames:
                - asset: The asset history DataFrame processed by PandasPart.
                - trade: The trade history DataFrame processed by PandasPart.
        """
        asset = PandasPart(self._history_asset, backword=True)
        trade = PandasPart(self._history_trade, backword=True)
        
        return asset, trade

    def calcMaxBuy(self, price):
        """
        Calculates the maximum number of asset units that can be purchased with the current balance at the given price.

        Args:
            price (int): The price per asset unit.

        Returns:
            int: The maximum number of asset units that can be bought.
        """
        return self._balance // price

    def calcMaxSell(self):
        """
        Calculates the maximum number of asset units that can be sold based on the current holdings.

        Returns:
            int: The maximum number of asset units available for sale.
        """
        return self._quantity

    def hold(self, reg_day, price):
        """
        Updates the account's total value based on the current price and quantity held,
        and records the current state in the asset history.

        Args:
            reg_day (str): The registration day of the record.
            price (int): The current price per asset unit.
        """
        self._account_price = price * self._quantity + self._balance
        self._average_price = 0 if self._quantity == 0 else int(self._invested / self._quantity)
        
        self._history_asset.loc[len(self._history_asset)] = {
            "reg_day": reg_day,
            "balance": self._balance,
            "quantity": self._quantity,
            "average_price": self._average_price,
            "invested": self._invested,
            "account": self._account_price
        }

    def buy(self, reg_day, price, quantity):
        """
        Executes a purchase of a specified quantity of assets at a given price,
        updates account balances, and records the trade.

        Args:
            reg_day (str): The registration day of the trade.
            price (int): The price per asset unit.
            quantity (int): The number of asset units to buy.
        """
        if quantity > 0:
            invested = int(price * quantity)  # Total cash used for purchasing
            buy_fee = int(invested * self._fee)  # Transaction fee for buying
            invested += buy_fee  # Total amount invested including fees
            rate = round(invested / self._balance * 100, 2)  # Percentage of balance used for purchase
            
            self._quantity += quantity
            self._invested += invested
            self._balance -= invested
        
            self._history_trade.loc[len(self._history_trade)] = {
                "reg_day": reg_day,
                "action": "buy",
                "price": price,
                "quantity": quantity,
                "fee": buy_fee,
                "tax": 0,
                "net_price": invested,
                "rate": rate,
            }
        self.hold(reg_day, price)

    def sell(self, reg_day, price, quantity):
        """
        Executes a sale of a specified quantity of assets at a given price,
        updates account balances, and records the trade.

        Args:
            reg_day (str): The registration day of the trade.
            price (int): The price per asset unit.
            quantity (int): The number of asset units to sell.
        """
        if quantity > 0:
            selled = int(price * quantity)  # Total amount obtained from selling
            sell_fee = int(selled * self._fee)  # Transaction fee for selling
            sell_tax = int(selled * self._tax)  # Transaction tax for selling
            selled -= sell_fee + sell_tax  # Net amount after fees and taxes
            rate = round(quantity / self._quantity * 100, 2)  # Percentage of total holdings sold
        
            self._invested -= int((self._invested / self._quantity) * quantity)
            self._quantity -= quantity
            self._balance += selled
            
            self._history_trade.loc[len(self._history_trade)] = {
                "reg_day": reg_day,
                "action": "sell",
                "price": price,
                "quantity": quantity,
                "fee": sell_fee,
                "tax": sell_tax,
                "net_price": selled,
                "rate": rate,
            }
        self.hold(reg_day, price)
