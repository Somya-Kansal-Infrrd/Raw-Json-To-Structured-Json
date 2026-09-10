"""MongoDB operations for mapping configuration."""

import json

from mongodb.mongo_template import mapping_collection


def load_mapping_file() -> dict:
    """Load field mappings from the JSON configuration file."""
    with open("field_mappings.json", "r") as file:
        return json.load(file)


def insert_mappings(data: dict) -> None:
    """Replace existing mappings with AUTO and MORTGAGE mappings."""
    auto_document = {
        "business_type": "AUTO",
        "mappings": data["autoFieldTransformationConfig"]
    }

    mortgage_document = {
        "business_type": "MORTGAGE",
        "mappings": data["mortgageFieldTransformationConfig"]
    }

    mapping_collection.delete_many({})
    mapping_collection.insert_many([
        auto_document,
        mortgage_document
    ])


def get_mapping(business_type: str) -> list[dict]:
    """Get mappings for the requested business type."""
    document = mapping_collection.find_one({
        "business_type": business_type
    })

    if not document:
        raise ValueError(
            f"No mapping found for {business_type}"
        )

    return document["mappings"]