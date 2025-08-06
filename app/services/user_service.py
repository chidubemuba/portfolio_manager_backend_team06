from functools import lru_cache
from collections import defaultdict

from app.models import db
from app.models.user import User
from app.models.stock import Stock

from app.services.yfinance_service import YFinanceService


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
    
