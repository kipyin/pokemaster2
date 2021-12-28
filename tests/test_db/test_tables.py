"""Tests for `pokemaster.database`."""
import peewee
import playhouse.test_utils
import pytest

from pokemaster2.db import tables as t

TEST_MODELS = [t.GrowthRates, t.Pokemon, t.PokemonSpecies]


def test_db_has_tables(empty_db: peewee.SqliteDatabase):
    """The database works."""
    tables = empty_db.get_tables()
    for model in TEST_MODELS:
        assert model._meta.table_name in tables


def test_database_empty(empty_db):
    """The database is empty at start."""
    with pytest.raises(peewee.DoesNotExist):
        t.Pokemon.get(id=1)


def test_add_pokemon_to_database(empty_db, pokemon_data):
    """t.Pokemon data can be added to the database."""
    assert 1 == t.Pokemon.get_by_id(1).id


def test_add_pokemon_species_to_database(empty_db, pokemon_species_data):
    """`t.PokemonSpecies` data can be added to the database."""
    assert 1 == t.PokemonSpecies.get_by_id(1).id


def test_call_species_from_pokemon(empty_db, pokemon_data, pokemon_species_data):
    """`t.Pokemon.species` should return a `t.PokemonSpecies`."""
    with playhouse.test_utils.count_queries() as query_counter:
        q = (
            t.Pokemon.select(t.Pokemon, t.PokemonSpecies)
            .join(t.PokemonSpecies)
            .where(t.Pokemon.id == 1)
            .first()
        )
        assert "bulbasaur" == q.species.identifier
    assert 1 == query_counter.count


def test_call_growth_rate_from_species(empty_db, pokemon_species_data, growth_rates_data):
    """`t.PokemonSpecies` joins the table `GrowthRate`."""
    with playhouse.test_utils.count_queries() as query_counter:
        q = (
            t.PokemonSpecies.select(t.PokemonSpecies, t.GrowthRates)
            .join(t.GrowthRates)
            .where(t.PokemonSpecies.id == 1)
            .first()
        )
        assert "medium-slow" == q.growth_rate.identifier
        assert 4 == q.growth_rate.id
    assert 1 == query_counter.count


def test_call_growth_rate_from_pokemon(
    empty_db, pokemon_data, pokemon_species_data, growth_rates_data
):
    """Call `t.Pokemon().species.growth_rate` and return a `GrowthRate` instance."""
    with playhouse.test_utils.count_queries() as query_counter:
        q = (
            t.Pokemon.select(t.Pokemon, t.PokemonSpecies, t.GrowthRates)
            .join(t.PokemonSpecies)
            .join(t.GrowthRates)
            .where(t.Pokemon.id == 1)
            .first()
        )
        assert isinstance(q, t.Pokemon)
        assert isinstance(q.species, t.PokemonSpecies)
        assert isinstance(q.species.growth_rate, t.GrowthRates)
        assert "medium-slow" == q.species.growth_rate.identifier
    assert 1 == query_counter.count


def test_get_pokemon(empty_db, pokemon_data, pokemon_species_data):
    """`get_pokemon` return a list of `t.Pokemon` data."""
    with playhouse.test_utils.count_queries() as query_counter:
        pokemon_set = t.get_pokemon("bulbasaur")
        pokemon = pokemon_set[0]
        assert 1 == len(pokemon_set)
        assert 1 == pokemon.species.id
    assert 1 == query_counter.count
