from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from ..models.user import create_user, find_user_by_email, verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(key in data for key in ["name", "email", "password"]):
        return jsonify({"error": "Name, email and password are required"}), 400
    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 409
    try:
        user_id = create_user(data["name"], data["email"], data["password"])
        token = create_access_token(identity=user_id)
        return (
            jsonify(
                {
                    "token": token,
                    "user": {
                        "id": user_id,
                        "name": data["name"],
                        "email": data["email"],
                    },
                }
            ),
            201,
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(key in data for key in ["email", "password"]):
        return jsonify({"error": "Email and password are required"}), 400
    user = find_user_by_email(data["email"])
    if not user or not verify_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user["_id"]))
    return (
        jsonify(
            {
                "token": token,
                "user": {
                    "id": str(user["_id"]),
                    "name": user["name"],
                    "email": user["email"],
                },
            }
        ),
        200,
    )


@auth_bp.route("/me", methods=["GET"])
def me():
    from flask_jwt_extended import get_jwt_identity, jwt_required

    @jwt_required()
    def inner():
        user_id = get_jwt_identity()
        return jsonify({"user_id": user_id}), 200

    return inner()
