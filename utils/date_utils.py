"""Date and timestamp utility functions."""

from datetime import datetime


def parse_timestamp(value: str | None) -> dict | None:
    """Convert a timestamp string to MongoDB date format."""
    if not value:
        return None

    dt = datetime.strptime(
        value,
        "%Y-%m-%d %H:%M:%S:%f"
    )

    return {
        "$date": dt.isoformat() + "Z"
    }