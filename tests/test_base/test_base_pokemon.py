"""Tests for `pokemaster2.pokemon`."""

import pytest

from pokemaster2.base.pokemon import BasePokemon
from pokemaster2.base.stats import Stats


@pytest.fixture(scope="function")
def test_base_pokemon():
    """A test instance of `BasePokemon`."""
    level = 50

    iv = Stats.max_iv()
    ev = Stats.zeros()
    base_stats = Stats.random_base_stats()
    stats = Stats.calc(level=level, base_stats=base_stats, iv=iv, ev=ev, nature="")
    stats_leveled_up = Stats.calc(level=level + 1, base_stats=base_stats, iv=iv, ev=ev, nature="")

    base_pokemon = BasePokemon(
        national_id=1,
        species="test_pokemon",
        form="default-form",
        types=["type_1", "type_2"],
        item_held="item",
        exp=10000,
        level=level,
        iv=iv,
        ev=ev,
        base_stats=stats,
        current_stats=stats,
        move_set=[],
        pid="",
        gender="male",
        nature="none",
        ability="none",
    )
    base_pokemon.level_up()
    assert 51 == base_pokemon.level
    assert stats_leveled_up == base_pokemon.stats
