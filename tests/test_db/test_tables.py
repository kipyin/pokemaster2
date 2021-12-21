"""Tests for `pokemaster.database`."""
import peewee
import pytest

from pokemaster2.db import tables
from pokemaster2.db.tables import MODELS, GrowthRates, Pokemon, PokemonSpecies


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


def test_add_pokemon_species_to_database(test_db, test_pokemon_species):
    """`PokemonSpecies` data can be added to the database."""
    assert 1 == test_pokemon_species.save()


def test_retrieve_pokemon_from_database(test_db, test_pokemon):
    """Pokemon data can be retrieved from the database."""
    test_pokemon_query = Pokemon.get(identifier="test-pokemon")
    assert "test-pokemon" == test_pokemon_query.identifier


def test_call_species_from_pokemon(test_db, test_pokemon, test_pokemon_species):
    """`Pokemon.species` should return a `PokemonSpecies`."""
    test_pokemon_species_query = (
        Pokemon.select(Pokemon, PokemonSpecies)
        .join(PokemonSpecies)
        .where(Pokemon.identifier == "test-pokemon")
        .first()
    )
    assert "test-species" == test_pokemon_species_query.species.identifier


def test_call_growth_rate_from_species(test_db, test_pokemon_species, test_growth_rate):
    """`PokemonSpecies` joins the table `GrowthRate`."""
    q = (
        PokemonSpecies.select(PokemonSpecies, GrowthRates)
        .join(GrowthRates)
        .where(PokemonSpecies.id == 1)
        .first()
    )
    assert "test-growth" == q.growth_rate.identifier


def test_call_growth_rate_from_pokemon(
    test_db, test_pokemon, test_pokemon_species, test_growth_rate
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


def test_get_pokemon(test_db, test_pokemon, test_pokemon_species):
    """`get_pokemon` return a list of `Pokemon` data."""
    pokemon_set = tables.get_pokemon("test-pokemon")
    pokemon = pokemon_set[0]
    assert 1 == len(pokemon_set)
    assert 1 == pokemon.species.id
