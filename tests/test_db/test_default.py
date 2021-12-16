"""Tests to `pokemaster2.db.defaults`."""

from pokemaster2.db import default


def test_get_default_db_uri_from_env(monkeypatch):
    """Default db uri can be set from the env var."""
    monkeypatch.setenv("POKEDEX_DB_ENGINE", "/path/to/db")
    uri, origin = default.db_uri_with_origin()
    assert "environment" == origin
    assert "/path/to/db" == uri


def test_get_default_csv_dir_from_env(monkeypatch):
    """Default csv path can be set from the env var."""
    monkeypatch.setenv("POKEDEX_CSV_PATH", "/path/to/csv")
    csv_path, origin = default.csv_dir_with_origin()
    assert "environment" == origin
    assert "/path/to/csv" == csv_path


def test_get_default_db_uri(monkeypatch):
    """Default db uri is `./data/pokedex.sqlite`."""
    monkeypatch.delenv("POKEDEX_DB_ENGINE", raising=False)
    uri, origin = default.db_uri_with_origin()
    assert "default" == origin
    assert uri.endswith("/data/pokedex.sqlite3")


def test_get_default_csv_dir(monkeypatch):
    """Default csv path is `./data/csv`."""
    monkeypatch.delenv("POKEDEX_CSV_PATH", raising=False)
    csv_path, origin = default.csv_dir_with_origin()
    assert "default" == origin
    assert csv_path.endswith("/data/csv")
