"""Given a seed, the PRNG should have the exact same behavior.

The seed and the results are from the following link:
https://www.smogon.com/ingame/rng/pid_iv_creation#pokemon_random_number_generator
"""

import pytest
from loguru import logger

from pokemaster2.prng import PRNG


def test_prng_generation_3():
    prng = PRNG(gen=3, seed=0)
    prng_1 = prng()
    logger.debug("PRNG seed: {seed}", seed=prng.seed)
    logger.debug("PRNG initial seed: {initial_seed}", initial_seed=prng._initial_seed)
    logger.debug("The first call of prng: {first_prng}", first_prng=prng_1)
    assert 59774 == prng()


def test_prng_generation_exception():
    prng = PRNG(gen=4)
    with pytest.raises(ValueError):
        prng()


def test_next_5():
    prng = PRNG(seed=0x1A56B091)
    assert prng.next_(4) == [0x01DB, 0x7B06, 0x5233, 0xE470]
    assert prng() == 0x5CC4


def test_reset_prng():
    prng = PRNG(seed=0)
    assert prng() == 0
    prng.next_(10)
    prng.reset()
    assert prng() == 0


def test_pid_ivs_creation():
    prng = PRNG(seed=0x560B9CE3)
    assert (0x7E482751, 0x5EE9629C) == prng.generate_pid_and_iv(method=2)


def test_randint():
    prng = PRNG(seed=0)
    prng()
    assert 19 == prng.randint(10, 20)
