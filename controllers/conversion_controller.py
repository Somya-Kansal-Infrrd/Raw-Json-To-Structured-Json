"""Controller for document conversion API."""

from flask import Blueprint, jsonify, request

from services.conversion.request_service import (
    validate_request,
    process_documents,
    save_output,
)


conversion_controller = Blueprint("conversion", __name__)


@conversion_controller.route("/api/convert", methods=["POST"])
def convert_api():
    """Handle document conversion requests."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "FAILURE",
                "error": "Request body is missing"
            }), 400

        error = validate_request(data)

        if error:
            return jsonify({
                "status": "FAILURE",
                "error": error
            }), 400

        result = process_documents(data)
        save_output(result)

        return jsonify({
            "status": "SUCCESS",
            "upload_request_id": data["requestId"],
            "documents_converted": len(result),
            "document_ids": [
                item["document_id"] for item in result
            ]
        }), 200

    except Exception as error:
        return jsonify({
            "status": "FAILURE",
            "error": str(error)
        }), 500