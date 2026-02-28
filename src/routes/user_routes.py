from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from services.log_service import log_activity

user_bp = Blueprint("users", __name__)


# Create User
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json

    user = User(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(user)
    db.session.commit()

    # Log in MongoDB
    log_activity("CREATE_USER", data)

    return jsonify(user.to_dict()), 201


# Get All Users
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# Get Single User
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


# Delete User
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    log_activity("DELETE_USER", {"user_id": user_id})

    return {"message": "User deleted"}