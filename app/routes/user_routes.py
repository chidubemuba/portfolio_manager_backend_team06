from flask import Blueprint, jsonify, request

from app.models import db
from app.models.user import User
from app.services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/', methods=['GET'])
def get_users():
    try:
        return jsonify(UserService.get_all_users()), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404


@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    try:
        return jsonify(UserService.get_user(id)), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404


@user_bp.route('/<int:id>/transactions', methods=['GET'])
def get_user_transactions(id):
    try:
        return jsonify(UserService.get_transactions(id)), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404


@user_bp.route('/<int:id>/holdings', methods=['GET'])
def get_user_holdings(id):
    try:
        return jsonify(UserService.get_holdings(id)), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404


@user_bp.route('/<int:id>/holdings/prices', methods=['GET'])
def get_user_holdings_current_prices(id):
    try:
        return jsonify(UserService.get_holdings_current_prices(id)), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404
    
    
@user_bp.route('/<int:id>/balance', methods=['GET'])
def get_user_balance(id):
    try:
        return jsonify(UserService.get_balance(id)), 200
    except IndexError as e:
        return jsonify({"message": str(e)}), 404
    

@user_bp.route('/<int:id>/deposit', methods=['POST'])
def deposit_user_balance(id):
    data = request.get_json()
    
    try:
        UserService.add_balance(id, data["ammount"])
        return jsonify({"message": "Balance updated successfully"}), 200
    except KeyError as e:
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400
    except IndexError as e:
        return jsonify({"message": str(e)}), 404
    

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    try:
        return UserService.create_user(
            f_name=data["f_name"], 
            l_name=data["l_name"],
            email=data["email"]
        ), 201
    except KeyError as e:
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400