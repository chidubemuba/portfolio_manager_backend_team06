from app.models import db
from app.models.holding import Holding
from app.models.transaction import Transaction
from app.models.stock import Stock

from app.services.user_service import UserService

class HoldingService:
    @classmethod
    def get_all_holdings(cls):
        holdings = Holding.query.all()
        
        if not holdings:
            raise IndexError("No active holdings found")
        
        return [holding.to_dict() for holding in holdings]
    
    
    @classmethod
    def add_security(cls, user_id: int, ticker: str, quantity: int) -> None:
        security = Holding.query.filter_by(user_id=user_id, ticker=ticker).first()
        
        if not security:
            print("Security not found in portfolio, adding new one")
            sec_name = Stock.query.get(ticker)
            security = Holding(user_id=user_id, ticker=ticker, asset_class=sec_name.asset_class, name=sec_name.name, quantity=0)
            db.session.add(security)
        
        security.quantity += quantity
        db.session.commit()
    
    
    @classmethod
    def reduce_security(cls, user_id: int, ticker: str, quantity: int) -> None:
        security = Holding.query.filter_by(user_id=user_id, ticker=ticker).first()
        
        if not security:
            raise KeyError("Security not found in portfolio")
        
        if security.quantity < quantity:
            raise OverflowError("Insufficient security quantity to reduce")
        
        security.quantity -= quantity
        
        if security.quantity == 0:
            print("Security quantity is 0, deleting from portfolio")
            db.session.delete(security)
        
        db.session.commit()

    @classmethod
    def calculate_avg_price(cls, new_transaction: Transaction) -> float:    
        user_transactions = UserService.get_transactions_of(new_transaction.user_id, new_transaction.ticker)
        holding = UserService.get_holding(new_transaction.user_id, new_transaction.ticker)

        if new_transaction.quantity < 0:
            return
                
        avg_price = new_transaction.price
                
        if holding:
            avg_price = sum(
                t["price"] * t["quantity"] for t in user_transactions if t["quantity"] > 0
            ) / sum(
                t["quantity"] for t in user_transactions
            )
                    
        holding.avg_price = avg_price            
        db.session.commit()
        return avg_price
