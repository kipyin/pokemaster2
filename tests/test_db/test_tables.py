"""Tests for `pokemaster.database`."""
import peewee
import pytest

from pokemaster2.db import tables
from pokemaster2.db.tables import MODELS, GrowthRates, Pokemon, PokemonSpecies


@pytest.fixture(autouse=True)
def empty_db():
    """Create, connect, and yield an empty database. Close after use."""
    db = peewee.SqliteDatabase(":memory:")
    db.bind(MODELS, bind_refs=True, bind_backrefs=True)
    db.connect()
    db.create_tables(MODELS)
    yield db
    db.drop_tables(MODELS)
    db.close()


@pytest.fixture
def bulbasaur():
    """Create a bulbasaur instance of `Pokemon`."""
    column_names = [
        "id",
        "identifier",
        "species_id",
        "height",
        "weight",
        "base_experience",
        "order",
        "is_default",
    ]
    data = [1, "bulbasaur", 1, 7, 69, 64, 1, 1]
    yield Pokemon.create(**dict(zip(column_names, data)))


@pytest.fixture
def bulbasaur_species():
    """Create a bulbasaur species instance of `PokemonSpecies`."""
    column_names = [
        "id",
        "identifier",
        "generation_id",
        "evolves_from_species_id",
        "evolution_chain_id",
        "color_id",
        "shape_id",
        "habitat_id",
        "gender_rate",
        "capture_rate",
        "base_happiness",
        "is_baby",
        "hatch_counter",
        "has_gender_differences",
        "growth_rate_id",
        "forms_switchable",
        "order",
        "conquest_order",
    ]
    data = [1, "bulbasaur", 1, None, 1, 5, 8, 3, 1, 45, 70, 0, 20, 0, 4, 0, 1]
    yield PokemonSpecies.create(**dict(zip(column_names, data)))


def test_db_has_tables(empty_db: peewee.SqliteDatabase):
    """The database works."""
    tables = empty_db.get_tables()
    for model in MODELS:
        assert model._meta.table_name in tables


def test_database_empty():
    """The database is empty at start."""
    with pytest.raises(peewee.DoesNotExist):
        Pokemon.get(id=1)


def test_add_pokemon_to_database(bulbasaur):
    """Pokemon data can be added to the database."""
    with pytest.raises(peewee.DoesNotExist):
        Pokemon.get(id=1)
    assert 1 == bulbasaur.save()


def test_add_pokemon_species_to_database(bulbasaur_species):
    """`PokemonSpecies` data can be added to the database."""
    assert 1 == bulbasaur_species.save()


def test_retrieve_pokemon_from_database(bulbasaur):
    """Pokemon data can be retrieved from the database."""
    q = Pokemon.get(id=1)
    assert "bulbasaur" == q.identifier


def test_call_species_from_pokemon(bulbasaur, bulbasaur_species):
    """`Pokemon.species` should return a `PokemonSpecies`."""
    q = Pokemon.select(Pokemon, PokemonSpecies).join(PokemonSpecies).where(Pokemon.id == 1).first()
    assert "bulbasaur" == q.species.identifier


def test_call_growth_rate_from_species(empty_db, test_pokemon_species, test_growth_rate):
    """`PokemonSpecies` joins the table `GrowthRate`."""
    q = (
        PokemonSpecies.select(PokemonSpecies, GrowthRates)
        .join(GrowthRates)
        .where(PokemonSpecies.id == 1)
        .first()
    )
    assert "test-growth" == q.growth_rate.identifier


def test_call_growth_rate_from_pokemon(
    empty_db, test_pokemon, test_pokemon_species, test_growth_rate
):
    """Call `Pokemon().species.growth_rate` and return a `GrowthRate` instance."""
    q = (
        Pokemon.select(Pokemon, PokemonSpecies, GrowthRates)
        .join(PokemonSpecies)
        .join(GrowthRates)
        .where(Pokemon.id == 1)
        .first()
    )
    assert isinstance(q, Pokemon)
    assert isinstance(q.species, PokemonSpecies)
    assert isinstance(q.species.growth_rate, GrowthRates)
    assert "test-growth" == q.species.growth_rate.identifier


def test_get_pokemon(empty_db, test_pokemon, test_pokemon_species):
    """`get_pokemon` return a list of `Pokemon` data."""
    pokemon_set = tables.get_pokemon("test-pokemon")
    pokemon = pokemon_set[0]
    assert 1 == len(pokemon_set)
    assert 1 == pokemon.species.id
