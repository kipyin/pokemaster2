"""Tests for `pokemaster.database`."""
import peewee
import playhouse.test_utils
import pytest

from pokemaster2.db import tables
from pokemaster2.db.tables import GrowthRates, Pokemon, PokemonSpecies

TEST_MODELS = [GrowthRates, Pokemon, PokemonSpecies]


@pytest.fixture()
def empty_db():
    """Create, connect, and yield an empty database. Close after use."""
    db = peewee.SqliteDatabase(":memory:")
    db.bind(TEST_MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables(TEST_MODELS)
    yield db
    db.drop_tables(TEST_MODELS)
    db.close()


@pytest.fixture(scope="function")
def bulbasaur(empty_db) -> Pokemon:
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
    q = Pokemon.create(**dict(zip(column_names, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def bulbasaur_species(empty_db) -> PokemonSpecies:
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
    q = PokemonSpecies.create(**dict(zip(column_names, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def medium_slow_growth(empty_db) -> GrowthRates:
    """Create a medium-slow GrowthRate instance."""
    column_names = ["id", "identifier", "formula"]
    data = [4, "medium-slow", r"\frac{6x^3}{5} - 15x^2 + 100x - 140"]
    q = GrowthRates.create(**dict(zip(column_names, data)))
    yield q
    q.delete_instance()


def test_db_has_tables(empty_db: peewee.SqliteDatabase):
    """The database works."""
    tables = empty_db.get_tables()
    for model in TEST_MODELS:
        assert model._meta.table_name in tables


def test_database_empty(empty_db):
    """The database is empty at start."""
    with pytest.raises(peewee.DoesNotExist):
        Pokemon.get(id=1)


def test_add_pokemon_to_database(empty_db, bulbasaur):
    """Pokemon data can be added to the database."""
    assert 1 == Pokemon.get_by_id(1).id


def test_add_pokemon_species_to_database(empty_db, bulbasaur_species):
    """`PokemonSpecies` data can be added to the database."""
    assert 1 == PokemonSpecies.get_by_id(1).id


def test_call_species_from_pokemon(empty_db, bulbasaur, bulbasaur_species):
    """`Pokemon.species` should return a `PokemonSpecies`."""
    with playhouse.test_utils.count_queries() as query_counter:
        q = (
            Pokemon.select(Pokemon, PokemonSpecies)
            .join(PokemonSpecies)
            .where(Pokemon.id == 1)
            .first()
        )
        assert "bulbasaur" == q.species.identifier
    assert 1 == query_counter.count


def test_call_growth_rate_from_species(empty_db, bulbasaur_species, medium_slow_growth):
    """`PokemonSpecies` joins the table `GrowthRate`."""
    with playhouse.test_utils.count_queries() as query_counter:
        q = (
            PokemonSpecies.select(PokemonSpecies, GrowthRates)
            .join(GrowthRates)
            .where(PokemonSpecies.id == 1)
            .first()
        )
        assert "medium-slow" == q.growth_rate.identifier
        assert 4 == q.growth_rate.id
    assert 1 == query_counter.count


def test_call_growth_rate_from_pokemon(empty_db, bulbasaur, bulbasaur_species, medium_slow_growth):
    """Call `Pokemon().species.growth_rate` and return a `GrowthRate` instance."""
    with playhouse.test_utils.count_queries() as query_counter:
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
        assert "medium-slow" == q.species.growth_rate.identifier
    assert 1 == query_counter.count


def test_get_pokemon(empty_db, bulbasaur, bulbasaur_species):
    """`get_pokemon` return a list of `Pokemon` data."""
    with playhouse.test_utils.count_queries() as query_counter:
        pokemon_set = tables.get_pokemon("bulbasaur")
        pokemon = pokemon_set[0]
        assert 1 == len(pokemon_set)
        assert 1 == pokemon.species.id
    assert 1 == query_counter.count
