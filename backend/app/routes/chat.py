import uuid

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models.chat import get_chat_history, get_sessions, save_message
from ..services.rag_service import get_rag_answer

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/ask", methods=["POST"])
@jwt_required(optional=True)
def ask():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data["query"].strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    user_id = get_jwt_identity() or "anonymous"
    session_id = data.get("session_id") or str(uuid.uuid4())
    history = []

    if user_id != "anonymous":
        history = get_chat_history(user_id, session_id)

    result = get_rag_answer(query, history)

    if user_id != "anonymous":
        save_message(user_id, session_id, "user", query, domain=result["domain"])
        save_message(
            user_id,
            session_id,
            "assistant",
            result["answer"],
            sources=result["sources"],
            domain=result["domain"],
        )

    return (
        jsonify(
            {
                "answer": result["answer"],
                "domain": result["domain"],
                "sources": result["sources"],
                "session_id": session_id,
            }
        ),
        200,
    )


@chat_bp.route("/history/<session_id>", methods=["GET"])
@jwt_required()
def history(session_id):
    user_id = get_jwt_identity()
    msgs = get_chat_history(user_id, session_id)
    return jsonify({"messages": msgs}), 200


@chat_bp.route("/sessions", methods=["GET"])
@jwt_required()
def sessions():
    user_id = get_jwt_identity()
    sess = get_sessions(user_id)
    return jsonify({"sessions": sess}), 200
