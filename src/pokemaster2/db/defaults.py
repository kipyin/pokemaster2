"""Database connection helpers."""
import os
from typing import Tuple


def get_default_db_uri_with_origin() -> Tuple[str, str]:
    """Determine the default db uri.

    Returns:
        Tuple[DB URI, the origin of the URI]
    """
    uri = os.environ.get("POKEDEX_DB_ENGINE", None)
    origin = "environment"

    if uri is None:
        import pkg_resources

        sqlite_path = pkg_resources.resource_filename("pokemaster2", "../data/pokedex.sqlite")
        uri = "sqlite:///" + sqlite_path
        origin = "default"

    return uri, origin


def get_default_csv_dir_with_origin() -> Tuple[str, str]:
    """Determine the default csv path.

    Returns:
        Tuple[CSV file path, the origin of the CSV path]
    """
    import pkg_resources

    csv_dir = pkg_resources.resource_filename("pokemaster2", "../data/csv")
    origin = "default"

    return csv_dir, origin


def get_default_db_uri() -> str:
    """Get only the default db uri, omitting the origin."""
    return get_default_db_uri_with_origin()[0]


def get_default_csv_dir() -> str:
    """Get only the default csv path, omitting the origin."""
    return get_default_csv_dir_with_origin()[0]
