"""Services for building document metadata."""

from utils.date_utils import parse_timestamp


def get_hierarchy_value(
    document: dict,
    classification_name: str
) -> str:
    """Get a value from document type hierarchy."""
    for item in document.get("docTypeHierarchy", []):
        if item.get("classificationName") == classification_name:
            return item.get("value", "").upper()

    return ""


def build_document_name(
    name: str,
    group_index: int
) -> str:
    """Add group number to document name."""
    if "." in name:
        filename, extension = name.rsplit(".", 1)
        return f"{filename}_{group_index + 1}.{extension}"

    return f"{name}_{group_index + 1}"


def is_list_document(document: dict) -> bool:
    """Check whether document is a list document."""
    for item in document.get("docTypeHierarchy", []):
        if item.get("classificationName") == "LIST_TYPE":
            value = item.get("value", "").upper()

            if value in ["LIST", "LIIST"]:
                return True

    return False

def build_metadata(
    document: dict,
    request_id: str,
    request_status: str,
    group_index: int
) -> dict:
    """Build metadata for a converted document."""
    return {
        "upload_request_id": request_id,
        "upload_request_status": request_status,
        "document_id": document["id"],
        "document_name": build_document_name(
            document["name"], group_index
        ),
        "document_file_type": document["fileType"],
        "document_processing_status": document["status"],
        "file_uploaded_timestamp": parse_timestamp(
            document.get("lastModifiedDate")
        ),
        "document_received_timestamp": parse_timestamp(
            document.get("documentReceivedDate")
        ),
        "document_extraction_start_timestamp": parse_timestamp(
            document.get("documentExtractionStartDate")
        ),
        "business_type": get_hierarchy_value(
            document, "CollateralType"
        ),
        "document_type": get_hierarchy_value(
            document, "DocumentType"
        ),
        "document_page_count": len(
            document.get("pages", [])
        ),
        "original_file_page_count": 0,
        "original_file_blank_pages": document.get(
            "totalBlankPages", 0
        ),
        "list_document": is_list_document(document),
        "optional_parameters": document.get(
            "optionalParams", {}
        ),
        "source_document_url": document.get(
            "sourceDocumentUrl"
        ),
        "account_id": None
    }