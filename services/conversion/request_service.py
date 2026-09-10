"""Services for handling conversion requests."""

import json

from services.conversion.conversion_service import convert_document


def validate_request(data: dict) -> str | None:
    """Validate required request fields."""
    for field in ["requestId", "status", "documents"]:
        if field not in data:
            return f"Missing {field}"
    return None


def get_business_type(document: dict) -> str:
    """Get business type from document hierarchy."""
    for item in document.get("docTypeHierarchy", []):
        if item.get("classificationName") == "CollateralType":
            return item.get("value", "").upper()
    return ""


def process_documents(data: dict) -> list[dict]:
    """Convert all documents in the request."""
    result = []

    for document in data["documents"]:
        business_type = get_business_type(document)

        if not business_type:
            continue

        result.extend(
            convert_document(
                document,
                business_type,
                data["requestId"],
                data["status"]
            )
        )

    return result


def save_output(documents: list) -> None:
    """Save converted documents to output JSON."""
    with open("output.json", "w") as file:
        json.dump(documents, file, indent=2)