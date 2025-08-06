from . import db

class Holding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    asset_class = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    avg_price = db.Column(db.Float, nullable=False, default=0.0)
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "name": self.name,
            "asset_class": self.asset_class,
            "quantity": self.quantity,
            "avg_price": self.avg_price,
            "user_id": self.user_id
        }
