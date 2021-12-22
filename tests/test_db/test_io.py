"""Tests for `pokemaseter2.io`."""
import peewee
import pytest

from pokemaster2.db import io, tables

TEST_MODELS = [tables.Pokemon]


@pytest.fixture
def unbound_db() -> peewee.SqliteDatabase:
    """Create and connect to an unbound db."""
    test_db = peewee.SqliteDatabase(":memory:")
    test_db.connect()
    yield test_db
    test_db.drop_tables(TEST_MODELS)
    test_db.close()


@pytest.fixture(scope="session")
def test_csv_dir(tmp_path_factory):
    """Create a temp path for `data/csv`."""
    csv_dir = tmp_path_factory.mktemp("data", numbered=False) / "csv"
    csv_dir.mkdir()
    yield csv_dir


@pytest.fixture(scope="function")
def test_pokemon_csv(test_csv_dir):
    """Create a temp pokemon CSV file in `data/csv/`."""
    content = """id,identifier,species_id,height,weight,base_experience,order,is_default
1,bulbasaur,1,7,69,64,1,1
"""
    pokemon_csv = test_csv_dir / "pokemon.csv"
    pokemon_csv.write_text(content)
    yield pokemon_csv


def test_load_unsafe(unbound_db, test_csv_dir):
    """Load db with `unsafe=True`."""
    io.load(unbound_db, csv_dir=test_csv_dir, models=[tables.Pokemon], safe=False, recursive=False)
    assert 0 == unbound_db.synchronous
    assert "memory" == unbound_db.journal_mode


def test_load_drop_table(unbound_db, test_csv_dir, test_pokemon_csv):
    """Drop tables."""
    # Load the pokemon table first
    io.load(unbound_db, models=TEST_MODELS, csv_dir=test_csv_dir)
    bulbasaur_1 = tables.Pokemon.select().where(tables.Pokemon.identifier == "bulbasaur").first()
    assert "bulbasaur" == bulbasaur_1.identifier

    # Drop the original pokemon table and load another table
    content = """id,identifier,species_id,height,weight,base_experience,order,is_default
1,bulbasaur_2,1,7,69,64,1,1
"""
    pokemon_csv = test_csv_dir / "pokemon.csv"
    pokemon_csv.write_text(content)
    io.load(unbound_db, models=[tables.Pokemon], csv_dir=test_csv_dir, drop_tables=True)
    bulbasaur_2 = tables.Pokemon.select().where(tables.Pokemon.identifier == "bulbasaur_2").first()
    assert "bulbasaur_2" == bulbasaur_2.identifier


def test_load_pokemon(unbound_db, test_pokemon_csv, test_csv_dir):
    """Load Pokemon."""
    io.load(unbound_db, models=[tables.Pokemon], csv_dir=test_csv_dir, drop_tables=True)
    bulbasaur = tables.Pokemon.select().where(tables.Pokemon.identifier == "bulbasaur").first()
    assert 1 == bulbasaur.id
