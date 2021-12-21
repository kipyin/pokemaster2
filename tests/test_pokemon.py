"""Tests for `pokemaster2.pokemon` module."""
from pokemaster2.pokemon import Stats


def test_stats_add() -> None:
    """Add two 'Stats' returns a new 'Stats'."""
    assert Stats(7, 7, 7, 7, 7, 7) == Stats(1, 2, 3, 4, 5, 6) + Stats(6, 5, 4, 3, 2, 1)


def test_stats_subtract():
    """Subtract one 'Stats' from another 'Stats' returns a new 'Stats'."""
    assert Stats(0, 0, 0, 0, 0, 0) == Stats(1, 1, 1, 1, 1, 1) - Stats(1, 1, 1, 1, 1, 1)


def test_stats_multiply():
    """Multiply two 'Stats' returns a new 'Stats'."""
    assert Stats(2, 4, 6, 8, 10, 12) == Stats(2, 2, 2, 2, 2, 2) * Stats(1, 2, 3, 4, 5, 6)


def test_stats_multiply_decimal():
    """Multiply two 'Stats' returns a new 'Stats'."""
    assert Stats(2, 4, 6, 8, 10, 12) == Stats(2.1, 2.1, 2.1, 2.1, 2.1, 2.1) * Stats(
        1, 2, 3, 4, 5, 6
    )


def test_stats_floor_division():
    """Floor division works on 'Stats' point-wise."""
    assert Stats(0, 1, 2, 2, 3, 4) == Stats(2, 4, 6, 8, 10, 12) // Stats(3, 3, 3, 3, 3, 3)


# @pytest.mark.xfail()
# def test_base_pokemon_from_pokedex_by_id():
#     """`BasePokemon` can be initialized from `pokedex` by national id."""
#     bulbasaur = BasePokemon._from_pokedex_by_id(national_id=1, level=1)
#     assert "bulbasaur" == bulbasaur.species
#     assert 1 == bulbasaur.level
#     assert ["grass"] == bulbasaur.types
