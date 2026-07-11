from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..services.doc_generator_service import generate_document, get_templates

generate_bp = Blueprint("generate", __name__)


@generate_bp.route("/templates", methods=["GET"])
def templates():
    return jsonify({"templates": get_templates()}), 200


@generate_bp.route("/document", methods=["POST"])
@jwt_required(optional=True)
def gen_document():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    template_id = data.get("template_id", "custom")
    fields = data.get("fields", {})
    custom_prompt = data.get("custom_prompt")

    if not custom_prompt and not fields:
        return jsonify({"error": "Provide fields or a custom_prompt"}), 400

    result = generate_document(template_id, fields, custom_prompt)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200
