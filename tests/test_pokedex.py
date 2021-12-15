"""Tests for `pokemaster.database`."""
import peewee
import pytest
from pokemaster2.pokedex import Pokemon, PokemonSpecies


MODELS = [Pokemon, PokemonSpecies]

@pytest.fixture
def session():
    db = peewee.SqliteDatabase(":memory:")
    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables(MODELS)
    yield db
    db.drop_tables(MODELS)
    db.close()


def null_test(session):
    """Test that the database works."""
    assert True
