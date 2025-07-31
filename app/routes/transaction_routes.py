from flask import Blueprint, jsonify, request
from datetime import datetime

from app.models import db
from app.models.transaction import Transaction

from app.services.transaction_service import TransactionService

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    try:
        return jsonify(TransactionService.get_all_transactions()), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404


@transaction_bp.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    try:
        return jsonify(TransactionService.get_transaction(id)), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404


@transaction_bp.route('/', methods=['POST'])
def new_transaction():
    data = request.get_json()
    
    new_transaction = Transaction(
        ticker=data["ticker"], 
        quantity=data["quantity"],
        price=data["price"],
        user_id=data["user_id"],
        timestamp=datetime.fromisoformat(data["timestamp"])
    )
    
    try: 
        return jsonify(TransactionService.place_order(new_transaction)), 201
    except KeyError as e:
        return jsonify({"message": str(e)}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
