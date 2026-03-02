from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {"error": "User not found"}, 404

    if not check_password_hash(user.password, data["password"]):
        return {"error": "Invalid password"}, 401

    token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return {
        "access_token": token,
        "role": user.role,
        "username": user.username
    }