from flask import Blueprint, jsonify, request

from app.models import db
from app.models.holding import Holding
from app.services.holding_service import HoldingService


holding_bp = Blueprint('holding_bp', __name__)


@holding_bp.route('/', methods=['GET'])
def get_holdings():
    try:
        return jsonify(HoldingService.get_all_holdings()), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404