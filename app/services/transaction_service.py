from app.models import db
from app.models.transaction import Transaction

from app.services.holding_service import HoldingService
from app.services.user_service import UserService
from app.services.yfinance_service import YFinanceService

class TransactionService:
    @classmethod
    def get_all_transactions(cls) -> list:
        transactions = Transaction.query.all()
        
        if not transactions:
            raise IndexError("No transactions found")
        
        return [t.to_dict() for t in transactions]
    
    
    @classmethod
    def get_transaction(cls, transaction_id: int) -> Transaction:
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            raise IndexError("Transaction not found")
        
        return transaction.to_dict()
    
    
    @classmethod
    def place_order(cls, transaction: Transaction) -> None:
        cls.__validate_transaction(transaction)
             
        if transaction.quantity < 0:
            UserService.add_balance(transaction.user_id, abs(transaction.quantity) * transaction.price)
            HoldingService.reduce_security(transaction.user_id, transaction.ticker, abs(transaction.quantity))
        else:
            UserService.reduce_balance(transaction.user_id, transaction.quantity * transaction.price)
            HoldingService.add_security(transaction.user_id, transaction.ticker, transaction.quantity)
        
        db.session.add(transaction)
        db.session.commit()
        
        HoldingService.calculate_avg_price(transaction)
        
        return transaction.to_dict()
    
    
    @classmethod
    def __validate_transaction(cls, transaction: Transaction) -> None:
        if transaction.price <= 0:
            raise ValueError("Price cannot be zero or negative")
        
        if transaction.quantity < 0:
            cls.__sell_validation(transaction)
        else:
            cls.__buy_validation(transaction)
            
        cls.__data_validation(transaction)
        
        print("Transaction validation passed")
        
        
    @classmethod
    def __sell_validation(cls, transaction: Transaction) -> None:
        holdings: list = UserService.get_holdings(transaction.user_id)
        
        user_holding = next((h for h in holdings if h["ticker"] == transaction.ticker), None)
        
        quantity = transaction.quantity
        
        if user_holding is None:
            raise KeyError("Stock not found in portfolio for selling")
        
        if user_holding["quantity"] < abs(quantity):
            raise ValueError("Insufficient stock quantity to sell")
        
        print("Sell validation passed")

    
    @classmethod
    def __buy_validation(cls, transaction: Transaction) -> None:
        balance = UserService.get_balance(transaction.user_id)

        if balance < transaction.quantity * transaction.price:
            raise ValueError("Insufficient balance to buy stock")
        
        print("Buy validation passed")
    
    
    @classmethod
    def __data_validation(cls, transaction: Transaction) -> None:
        if YFinanceService.get_stock_data(transaction.ticker).empty:
            raise KeyError(f"Ticker: {transaction.ticker} not found in market")
        
        print("Data validation passed")
    