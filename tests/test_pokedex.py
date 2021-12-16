"""Tests for `pokemaster.database`."""
import peewee
import pytest

from pokemaster2.pokedex import Pokemon, PokemonSpecies

MODELS = [Pokemon, PokemonSpecies]


@pytest.fixture
def test_db():
    db = peewee.SqliteDatabase(":memory:")
    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables(MODELS)
    yield db
    db.drop_tables(MODELS)
    db.close()


def test_sanity(test_db):
    """The database works."""
    assert True
