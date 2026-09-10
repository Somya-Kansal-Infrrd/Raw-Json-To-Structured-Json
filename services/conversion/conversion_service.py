"""Main document conversion service."""

from services.field.field_service import convert_field
from services.metadata.metadata_service import build_metadata


def convert_document(
    document: dict,
    business_type: str,
    request_id: str,
    request_status: str
) -> list[dict]:
    """Convert one document into output documents."""
    mappings = _get_mappings(business_type)
    lookup = {
        mapping["titanFieldName"]: mapping
        for mapping in mappings
    }

    object_list = _find_object_list(document)
    groups = object_list["values"] if object_list else [[]]

    common_fields = _convert_common_fields(
        document["fields"],
        object_list,
        lookup
    )

    return _build_outputs(
        document,
        groups,
        common_fields,
        lookup,
        request_id,
        request_status
    )


def _get_mappings(business_type: str) -> list[dict]:
    """Get mappings for a business type."""
    from mongodb.mongo_operation import get_mapping

    return get_mapping(business_type)


def _find_object_list(document: dict) -> dict | None:
    """Find the object-list field."""
    return next(
        (
            field for field in document["fields"]
            if field["type"].lower() == "object list"
        ),
        None
    )


def _convert_common_fields(
    fields: list,
    object_list: dict | None,
    lookup: dict
) -> list[dict]:
    """Convert fields outside the object list."""
    result = []

    for field in fields:
        if field is object_list:
            continue

        converted = convert_field(field, lookup)

        if converted:
            result.append(converted)

    return result


def _build_outputs(
    document: dict,
    groups: list,
    common_fields: list,
    lookup: dict,
    request_id: str,
    request_status: str
) -> list[dict]:
    """Build output for each object-list group."""
    from services.field.object_list_service import (
        convert_object_list
    )

    outputs = []

    for index, group in enumerate(groups):
        metadata = build_metadata(
            document,
            request_id,
            request_status,
            index
        )

        metadata["fields"] = (
            common_fields +
            convert_object_list(group, lookup)
        )

        outputs.append(metadata)

    return outputs