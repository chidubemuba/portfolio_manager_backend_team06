from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    holdings = db.relationship('Holding', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
            "balance": self.balance
        }
