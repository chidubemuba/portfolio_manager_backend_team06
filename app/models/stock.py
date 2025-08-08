from . import db

class Stock(db.Model):
    __tablename__ = "stock"

    ticker = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    asset_class = db.Column(db.String(50), nullable=False)
    sector = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "name": self.name,
            "asset_class": self.asset_class,
            "sector": self.sector,
        }
