from flask import Blueprint, jsonify, request

from app.models import db
from app.models.transaction import Transaction

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    
    if not transactions:
        return jsonify({"message": "No transactions found"}), 404
    
    return jsonify([t.to_dict() for t in transactions]), 200


@transaction_bp.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get(id)
    
    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404
    
    return jsonify(transaction.to_dict()), 200


@transaction_bp.route('/', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    
    new_transaction = Transaction(
        ticker=data["ticker"], 
        quantity=data["quantity"],
        timestamp=data["timestamp"]
    )
    
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction.to_dict()), 201
