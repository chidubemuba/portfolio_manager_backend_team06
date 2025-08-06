from functools import lru_cache
from collections import defaultdict

from app.models import db
from app.models.user import User
from app.models.stock import Stock

from app.services.yfinance_service import YFinanceService
from collections import defaultdict,deque


class UserService:
    @classmethod
    def get_user(cls, user_id: int):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        return user.to_dict()
    
    @classmethod
    def get_all_users(cls):
        users = User.query.all()
    
        if not users:
            raise IndexError("No active users found")

        return [u.to_dict() for u in users]
    
    
    @classmethod
    def create_user(cls, f_name: str, l_name: str, email: str) -> User:
        new_user = User(f_name=f_name, l_name=l_name, email=email)
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.to_dict()
    
    
    @classmethod
    def get_balance(cls, user_id: int) -> float:
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        return user.balance
    
    
    @classmethod
    def add_balance(cls, user_id: int, ammount: float) -> None:
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")

        user.balance += ammount
        db.session.commit()
        
    
    @classmethod
    def reduce_balance(cls, user_id: int, ammount: float) -> None:
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        if user.balance < ammount:
            raise ValueError("Insufficient balance")
        
        user.balance -= ammount
        db.session.commit()

    
    @classmethod
    def get_holdings(cls, user_id: int):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        if not user.holdings:
            return []
        
        return [h.to_dict()for h in user.holdings]
    

    @classmethod
    def get_unrealized_gains(cls, user_id: int):
        user = User.query.get(user_id)

        if not user:
            raise IndexError("User not found")
        
        if not user.holdings:
            return []
        current_prices = UserService.get_holdings_current_prices(user_id)
    
        total_cost = 0.0
        total_current_value = 0.0
    
        for holding in user.holdings:
            ticker = holding.ticker
            quantity = holding.quantity
            average_price = holding.avg_price

            # Skip if ticker not found in current prices
            if ticker not in current_prices:
                continue

            current_price = current_prices[ticker]

            total_cost += quantity * average_price
            total_current_value += quantity * current_price

        if total_cost == 0:
            return 0.0  

        gain_percent = ((total_current_value - total_cost) / total_cost) * 100 
        return gain_percent
    
    
    @classmethod
    def get_realized_gains(cls, user_id: int):
        user = User.query.get(user_id)

        if not user:
            raise IndexError("User not found")
        
        if not user.transactions:

            return []

    
        buy_queues = defaultdict(deque)
        realized_gain = 0
        realized_cost_basis = 0

        for transaction in user.transactions:
            ticker = transaction.ticker
            qty = transaction.quantity
            price = transaction.price

            if qty > 0:
                buy_queues[ticker].append({'quantity': qty, 'price': price})
            else:
                sell_qty = -qty
                while sell_qty > 0:
                    if not buy_queues[ticker]:
                        raise Exception(f"Trying to sell more {ticker} than owned.")

                    lot = buy_queues[ticker][0]
                    lot_qty = lot['quantity']
                    buy_price = lot['price']

                    match_qty = min(sell_qty, lot_qty)

                    gain = (price - buy_price) * match_qty
                    cost_basis = buy_price * match_qty

                    realized_gain += gain
                    realized_cost_basis += cost_basis

                    if match_qty == lot_qty:
                        buy_queues[ticker].popleft()
                    else:
                        lot['quantity'] -= match_qty

                    sell_qty -= match_qty

        if realized_cost_basis == 0:
            gain_percent = 0
        else:
            gain_percent = (realized_gain / realized_cost_basis) * 100
        return gain_percent
    
    
    @classmethod
    def get_holdings_current_prices(cls, user_id: int):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        if not user.holdings:
            return []
        
        data = {}
        for holding in user.holdings:
            symbol = holding.to_dict().get("ticker", None)
            
            if symbol is None:
                raise IndexError("Ticker not found")
            
            data[symbol] = YFinanceService.get_current_price(symbol)
        
        return data
    
    
    @classmethod
    def get_holding(cls, user_id: int, ticker: str = None):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        holding = next((h for h in user.holdings if h.ticker == ticker), None)
        return holding
    
    
    @classmethod
    @lru_cache()
    def get_asset_alloc(cls, user_id: int):
        holdings = cls.get_holdings(user_id)
        
        total_val = 0
        data = defaultdict(float)
        for holding in holdings:
            quantity = holding['quantity']
            stock = Stock.query.get(holding['ticker'].upper())
            current_price = YFinanceService.get_current_price(stock.ticker)
            value = quantity * current_price
            
            total_val += value
            data[stock.asset_class] += value
        
        cash = cls.get_balance(user_id)
        data['cash'] = cash
        total_val += cash
        
        return {k:round((v/total_val*100), 2) for k, v in data.items()}
            
    
    @classmethod
    def get_transactions(cls, user_id: int):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        if not user.transactions:
            return []
        
        return [t.to_dict() for t in user.transactions]
    
    
    @classmethod
    def get_transactions_of(cls, user_id: int, ticker: str):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        transactions = [t.to_dict() for t in user.transactions if t.ticker == ticker]
        
        return transactions
    
