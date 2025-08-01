from flask import Blueprint, jsonify, request

from app.models import db
from app.services.yfinance_service import YFinanceService


data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/', methods=['GET'])
def get_available_tickers():
    try:
        tickers = YFinanceService.get_available_tickers()
        return jsonify(tickers), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@data_bp.route('/<string:ticker>', methods=['GET'])
def get_ticker_data(ticker):
    
    try: 
        return YFinanceService.get_stock_data(ticker).to_json(), 200
    except KeyError as e:
        return jsonify({"message": str(e)}), 404
    
