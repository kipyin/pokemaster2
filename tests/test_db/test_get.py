"""Tests for `pokemaster2.db.get`."""
from playhouse import test_utils

from pokemaster2.db import get
from pokemaster2.db import tables as t


def test_get_pokemon(empty_db, bulbasaur, bulbasaur_species, growth_medium_slow):
    """Get Pokemon by species ID."""
    with test_utils.count_queries() as query_counter:
        q = get.pokemon(1)
        assert isinstance(q, t.Pokemon)
        assert isinstance(q.species, t.PokemonSpecies)
        assert isinstance(q.species.growth_rate, t.GrowthRates)
    # get.pokemon is lazy
    assert 3 == query_counter.count


def test_pokedex_entry(
    empty_db,
    bulbasaur,
    bulbasaur_species,
    bulbasaur_name,
    bulbasaur_flavor_text,
    language_english,
    version_red,
):
    """Get a pokedex entry."""
    q = get.pokedex_entry(pokemon_id=1, language="en", version="red")
    assert 1 == q.species_id
    assert "Bulbasaur" == q.name
    assert "Seed Pokémon" == q.genus


def test_pokemon_types(
    empty_db,
    bulbasaur_types,
    types,
):
    """Get a pokemon's types."""
    pokemon_types = get.pokemon_types(1)
    assert 2 == len(pokemon_types)
    assert ["grass", "poison"] == [x.identifier for x in pokemon_types]


def test_pokemon_evolution_chain(
    empty_db,
    bulbasaur_species,
    bulbasaur_name,
    ivysaur_species,
    ivysaur_name,
    venusaur_species,
    venusaur_name,
    language_english,
):
    """`pokemon_evolution_chain` return a tree."""
    tree = get.pokemon_evolution_chain(pokemon_id=3, language="en")
    assert {(1, "Bulbasaur", None): {(2, "Ivysaur", 1): {(3, "Venusaur", 2): {}}}} == tree
