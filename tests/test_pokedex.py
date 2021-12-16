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


@pytest.fixture
def test_pokemon():
    yield Pokemon.create(
        id=1,
        identifier="test_pokemon",
        species="test_pokemon",
        height=10,
        weight=10,
        base_experience=100,
        order=1,
        is_default=True,
    )


def test_sanity(test_db):
    """The database works."""
    assert True


def test_add_pokemon_to_database(test_db, test_pokemon):
    """Pokemon data can be added to the database."""
    assert 1 == test_pokemon.save()


def test_retrieve_pokemon_from_database(test_db, test_pokemon):
    """Pokemon data can be retrieved from the database."""
    test_pokemon.save()
    assert "test_pokemon" == Pokemon.get(identifier="test_pokemon").identifier
