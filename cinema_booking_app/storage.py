"""Safe JSON file access for movies and bookings."""

import json
import os
import tempfile


class StorageError(Exception):
    """Raised when application data cannot be read or saved."""


def load_json(path, default):
    """Load JSON data, returning a default only when the file does not exist."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as data_file:
            return json.load(data_file)
    except json.JSONDecodeError as error:
        raise StorageError(f"The data file is damaged: {path}") from error
    except OSError as error:
        raise StorageError(f"The data file could not be opened: {path}") from error


def save_json(path, data):
    """Save JSON atomically so an interrupted write does not damage the file."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=folder, delete=False
        ) as temporary_file:
            json.dump(data, temporary_file, indent=2)
            temporary_path = temporary_file.name
        os.replace(temporary_path, path)
    except OSError as error:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)
        raise StorageError(f"The data file could not be saved: {path}") from error
