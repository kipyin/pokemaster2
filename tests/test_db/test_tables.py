"""Tests for `pokemaster.database`."""
import peewee
import pytest

from pokemaster2.db import tables
from pokemaster2.db.tables import MODELS, Pokemon, PokemonSpecies


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
def test_pokemon_species():
    test_pokemon_species = PokemonSpecies.create(
        id=1,
        identifier="test-species",
        evolves_from=None,
        gender_rate=8,
        capture_rate=255,
        base_happiness=0,
        is_baby=False,
        hatch_counter=10,
        has_gender_differences=False,
        forms_switchable=False,
        order=1,
        conquest_order=1,
    )
    yield test_pokemon_species


@pytest.fixture
def test_pokemon(test_pokemon_species):
    test_pokemon_species.save()
    yield Pokemon.create(
        id=1,
        identifier="test-pokemon",
        species=test_pokemon_species,
        height=10,
        weight=10,
        base_experience=100,
        order=1,
        is_default=True,
    )


def test_db_has_tables(test_db):
    """The database works."""
    tables = test_db.get_tables()
    for model in MODELS:
        assert model._meta.table_name in tables


def test_database_empty(test_db):
    """The database is empty at start."""
    with pytest.raises(peewee.DoesNotExist):
        Pokemon.get(id=1)


def test_add_pokemon_to_database(test_db, test_pokemon):
    """Pokemon data can be added to the database."""
    assert 1 == test_pokemon.save()


def test_pokemon_species_is_saved_with_pokemon(test_db, test_pokemon):
    """`PokemonSpecies` is saved when `Pokemon` is saved."""
    test_pokemon.save()
    assert 1 == PokemonSpecies.get(id=1).id


def test_add_pokemon_species_to_database(test_db, test_pokemon_species):
    """`PokemonSpecies` data can be added to the database."""
    assert 1 == test_pokemon_species.save()


def test_retrieve_pokemon_from_database(test_db, test_pokemon):
    """Pokemon data can be retrieved from the database."""
    test_pokemon.save()
    test_pokemon_query = Pokemon.get(identifier="test-pokemon")
    assert "test-pokemon" == test_pokemon_query.identifier


def test_call_species_from_pokemon(test_db, test_pokemon):
    """`Pokemon.species` should return a `PokemonSpecies`."""
    test_pokemon.save()
    test_pokemon_species_query = (
        Pokemon.select(Pokemon, PokemonSpecies)
        .join(PokemonSpecies)
        .where(Pokemon.identifier == "test-pokemon")
        .first()
    )
    assert "test-species" == test_pokemon_species_query.species.identifier


def test_get_pokemon(test_db, test_pokemon):
    """`get_pokemon` return a list of `Pokemon` data."""
    test_pokemon.save()
    pokemon_set = tables.get_pokemon("test-pokemon")
    pokemon = pokemon_set[0]
    assert 1 == len(pokemon_set)
    assert 1 == pokemon.species.id
