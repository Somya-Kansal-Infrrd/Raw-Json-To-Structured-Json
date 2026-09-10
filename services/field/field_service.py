"""Services for converting document fields."""


def resolve_value(field: dict) -> str:
    """Get the actual value from a field."""
    if field["dataType"].lower() == "dropdown":
        value_obj = field["valueObject"]
        return value_obj.get("dropdownValue", "").strip()

    return field["value"]


def convert_data_type(data_type: str) -> str:
    """Convert source data type to output data type."""
    if data_type == "string":
        return "String"

    return data_type


def convert_field(
    field: dict,
    mapping_lookup: dict
) -> dict | None:
    """Convert a common field using its mapping."""
    mapping = mapping_lookup.get(field["name"])

    if not mapping:
        return None

    return {
        "field_name": mapping["customFormatFieldName"],
        "field_value": resolve_value(field),
        "field_type": field["type"],
        "field_data_type": convert_data_type(
            field["dataType"]
        ),
    }


def convert_object_list(
    group: list,
    mapping_lookup: dict
) -> list[dict]:
    """Convert fields belonging to an object-list group."""
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