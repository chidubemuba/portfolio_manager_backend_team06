from . import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ticker = db.Column(db.String(50), db.ForeignKey('stock.ticker'), nullable=False)
    ticker = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "quantity": self.quantity,
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }
