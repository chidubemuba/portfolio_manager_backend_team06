from . import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(50), db.ForeignKey('stock.ticker'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "quantity": self.quantity,
            "timestamp": self.timestamp
        }
