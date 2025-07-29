from . import db

class Stock(db.Model):
    ticker = db.Column(db.String(50), primary_key=True)

    def to_dict(self):
        return {
            "ticker": self.ticker,
        }
