from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..services.upload_service import (
    delete_document,
    ingest_document,
    list_user_documents,
    query_user_documents,
)

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
@jwt_required(optional=True)
def upload_document():
    user_id = get_jwt_identity() or "anonymous"
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if not file.filename or not _allowed(file.filename):
        return jsonify({"error": "Invalid file. Use PDF, DOCX, or TXT."}), 400
    file_bytes = file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        return jsonify({"error": "File too large. Max 10 MB."}), 400
    try:
        result = ingest_document(user_id, file_bytes, file.filename)
        return jsonify({"success": True, **result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": f"Processing failed: {e}"}), 500


@upload_bp.route("/documents", methods=["GET"])
@jwt_required(optional=True)
def list_documents():
    user_id = get_jwt_identity() or "anonymous"
    docs = list_user_documents(user_id)
    return jsonify({"documents": docs}), 200


@upload_bp.route("/documents/<doc_id>", methods=["DELETE"])
@jwt_required(optional=True)
def delete_doc(doc_id):
    user_id = get_jwt_identity() or "anonymous"
    success = delete_document(user_id, doc_id)
    if success:
        return jsonify({"success": True}), 200
    return jsonify({"error": "Document not found"}), 404


@upload_bp.route("/query", methods=["POST"])
@jwt_required(optional=True)
def query_documents():
    user_id = get_jwt_identity() or "anonymous"
    data = request.get_json()
    if not data or not data.get("query"):
        return jsonify({"error": "Query is required"}), 400
    result = query_user_documents(
        user_id=user_id,
        query=data["query"],
        doc_id=data.get("doc_id"),
    )
    return jsonify(result), 200
