from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models.expert import book_expert, get_all_experts, seed_experts

expert_bp = Blueprint("expert", __name__)


@expert_bp.before_app_request
def init_experts():
    pass


@expert_bp.route("/", methods=["GET"])
def experts():
    seed_experts()
    domain = request.args.get("domain")
    data = get_all_experts(domain)
    return jsonify({"experts": data}), 200


@expert_bp.route("/book", methods=["POST"])
@jwt_required()
def book():
    user_id = get_jwt_identity()
    data = request.get_json()
    required = ["expert_id", "date", "time_slot"]
    if not all(key in data for key in required):
        return jsonify({"error": "Missing required fields"}), 400
    booking_id = book_expert(
        user_id,
        data["expert_id"],
        data["date"],
        data["time_slot"],
        data.get("query_summary", ""),
    )
    return jsonify({"booking_id": booking_id, "message": "Booking confirmed!"}), 201
