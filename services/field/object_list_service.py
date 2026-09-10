"""Service for converting object-list fields."""

from services.field.field_service import (
    convert_data_type,
    resolve_value,
)


def convert_object_list(
    group: list,
    mapping_lookup: dict
) -> list[dict]:
    """Convert fields belonging to one object-list group."""
    group_fields = []

    shared_object_id = (
        group[0].get("objectId") if group else None
    )

    for subfield in group:
        mapping = mapping_lookup.get(
            subfield["fieldName"]
        )

        if not mapping:
            continue

        group_fields.append({
            "field_name": mapping["customFormatFieldName"],
            "field_value": resolve_value(subfield),
            "field_type": subfield["fieldType"],
            "field_data_type": convert_data_type(
                subfield["dataType"]
            ),
            "titan_field_name": subfield["fieldName"],
            "titan_field_id": subfield.get("fieldId"),
            "titan_object_id": subfield.get(
                "objectId",
                shared_object_id
            )
        })

    return group_fields