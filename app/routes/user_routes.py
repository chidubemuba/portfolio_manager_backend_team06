from flask import Blueprint, jsonify, request

from app.models import db
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    
    if not users:
        return jsonify({"message": "No active portfolio found"}), 404
    
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.route('/<int:id>', methods=['GET'])
def get_user():
    user = User.query.get(id)
    
    if not user :
        return jsonify({"message": "No active portfolio found"}), 404
    
    return jsonify(user.to_dict()), 200


@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User(
        f_name=data["f_name"], 
        l_name=data["l_name"],
        email=data["email"]
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201