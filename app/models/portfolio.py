from . import db

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user = db.Column(db.Integer, db.ForeignKey('user.id')) #, nullable=False)
    ticker = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "quantity": self.quantity,
            "user_id": self.user_id
        }
