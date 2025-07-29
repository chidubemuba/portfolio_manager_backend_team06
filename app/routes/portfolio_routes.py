from flask import Blueprint, jsonify, request

from app.models import db
from app.models.portfolio import Portfolio


portfolio_bp = Blueprint('portfolio_bp', __name__)


@portfolio_bp.route('/', methods=['GET'])
def get_portfolio():
    portfolio = Portfolio.query.all()
    
    if not portfolio:
        return jsonify({"message": "No active portfolio found"}), 404
    
    return jsonify([p.to_dict() for p in portfolio]), 200


@portfolio_bp.route('/', methods=['POST'])
def create_portfolio():
    data = request.get_json()

    new_portfolio = Portfolio(
        ticker=data["ticker"], 
        quantity=data["quantity"],
        user_id=data["user_id"]
    )
    
    db.session.add(new_portfolio)
    db.session.commit()
    return jsonify(new_portfolio.to_dict()), 201


@portfolio_bp.route('/<string:ticker>', methods=['DELETE'])
def delete_portfolio(ticker):
    portfolio = Portfolio.query.filter_by(ticker=ticker).first()
    
    if not portfolio:
        return jsonify({"message": "No active portfolio found"}), 404
    
    db.session.delete(portfolio)
    db.session.commit()
    
    return jsonify({"message": f"Deleted holding: {ticker}"}), 200
