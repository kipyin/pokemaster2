"""Tests for pokemaster2.dna module."""
from pokemaster2.base.dna import DNA


def test_random_dna_consistency():
    """A DNA generated randomly should be self-consistent."""
    random_dna = DNA.random()
    assert random_dna.pid % 25 == random_dna.nature_index
    assert random_dna.pid % 2 == random_dna.ability_index
    assert random_dna.pid % 255 == random_dna.gender_index
