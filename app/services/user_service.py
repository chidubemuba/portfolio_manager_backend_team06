from app.models import db
from app.models.user import User
from app.models.holding import Holding
from app.models.transaction import Transaction


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
    def get_transactions(cls, user_id: int):
        user = User.query.get(user_id)
        
        if not user:
            raise IndexError("User not found")
        
        if not user.transactions:
            return []
        
        return [t.to_dict() for t in user.transactions]
    
