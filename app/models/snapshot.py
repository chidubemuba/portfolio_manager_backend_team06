from . import db

class Snapshot(db.Model):
    __tablename__ = "snapshot"
    __table_args__ = (
        db.UniqueConstraint("date", name="uix_date"),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    date = db.Column(db.DateTime, nullable=False)    
    portfolio_value = db.Column(db.Float, nullable=False)
    cash_balance = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def to_dict(self):
        return {
            "date": self.date,
            "portfolio_value": self.portfolio_value,
            "cash_balance": self.cash_balance
        }
