"""Database connection helpers."""
import os
from typing import Tuple


def db_uri_with_origin() -> Tuple[str, str]:
    """Determine the default db uri.

    Returns:
        Tuple[DB URI, the origin of the URI]
    """
    uri = os.environ.get("POKEDEX_DB_ENGINE", None)
    origin = "environment"

    if uri is None:
        import importlib_resources

        sqlite_path = importlib_resources.files("pokemaster2").parent / "data/pokedex.sqlite3"
        uri = "sqlite:///" + str(sqlite_path)
        origin = "default"

    return uri, origin


def csv_dir_with_origin() -> Tuple[str, str]:
    """Determine the default csv path.

    Returns:
        Tuple[CSV file path, the origin of the CSV path]
    """
    csv_path = os.environ.get("POKEDEX_CSV_PATH", None)
    origin = "environment"

    if csv_path is None:
        import importlib_resources

        csv_path = str(importlib_resources.files("pokemaster2").parent / "data/csv")
        origin = "default"

    return csv_path, origin


def db_uri() -> str:
    """Get only the default db uri, omitting the origin."""
    return db_uri_with_origin()[0]


def csv_dir() -> str:
    """Get only the default csv path, omitting the origin."""
    return csv_dir_with_origin()[0]
