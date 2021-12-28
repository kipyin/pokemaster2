"""Tests for `pokemaster2.db.get`."""
from playhouse import test_utils

from pokemaster2.db import get
from pokemaster2.db import tables as t
from pokemaster2.stats import Stats


def test_get_pokemon(empty_db, pokemon_data, pokemon_species_data, growth_rates_data):
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
    pokemon_data,
    pokemon_species_data,
    pokemon_species_name_data,
    pokemon_species_flavor_text_data,
    language_data,
    version_data,
):
    """Get a pokedex entry."""
    q = get.pokedex_entry(pokemon_id=1, language="en", version="red")
    assert 1 == q.species_id
    assert "Bulbasaur" == q.name
    assert "Seed Pokémon" == q.genus


def test_pokemon_types(empty_db, pokemon_types_data, types_data):
    """Get a pokemon's types."""
    pokemon_types = get.pokemon_types(1)
    assert 2 == len(pokemon_types)
    assert ["grass", "poison"] == [x.identifier for x in pokemon_types]


def test_pokemon_evolution_chain(
    empty_db,
    pokemon_species_data,
    pokemon_species_name_data,
    language_data,
):
    """`pokemon_evolution_chain` return a tree."""
    tree = get.pokemon_evolution_chain(pokemon_id=3, language="en")
    assert {(1, "Bulbasaur", None): {(2, "Ivysaur", 1): {(3, "Venusaur", 2): {}}}} == tree


def test_pokemon_by_identifier(
    empty_db,
    pokemon_data,
    pokemon_species_data,
):
    q = get.pokemon_by_identifier(identifier="bulbasaur")
    assert 1 == q.id


def test_pokemon_by_id_or_identifier(
    empty_db,
    pokemon_data,
    pokemon_species_data,
):
    q = get.pokemon(1)
    assert 1 == q.id
    q = get.pokemon("bulbasaur")
    assert 1 == q.id


def test_base_stats_and_ev_yields(empty_db, pokemon_stats_data, pokemon_forms_data, pokemon_data):
    """Get Pokémon's base stats and ev yields from the database."""
    base_stats, ev_yields = get.base_stats_and_ev_yields(species_id=1, form=None)
    assert Stats(45, 49, 49, 65, 65, 45) == base_stats
    assert Stats(0, 0, 0, 1, 0, 0) == ev_yields
