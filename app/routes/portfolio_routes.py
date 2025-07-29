from flask import Blueprint, jsonify, request
import uuid

from app.models import db
from app.models.portfolio import Portfolio

portfolio_bp = Blueprint('portfolio_bp', __name__)

@portfolio_bp.route('/', methods=['GET'])
def get_portfolio():
    portfolio = Portfolio.query.first() # TODO: Change this
    
    if not portfolio:
        return jsonify({"message": "No active portfolio found"}), 404
    
    return jsonify(portfolio), 200


@portfolio_bp.route('/', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    
    new_portfolio = Portfolio(
        ticker=data["ticker"], 
        quantity=data["quantity"]
    )
    
    db.session.add(new_portfolio)
    db.session.commit()
    return jsonify(new_portfolio.to_dict()), 201
