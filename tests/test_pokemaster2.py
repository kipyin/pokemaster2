"""Tests for `pokemaster2` module."""
from typing import Generator

import pytest

import pokemaster2


@pytest.fixture
def version() -> Generator[str, None, None]:
    """Sample pytest fixture."""
    yield pokemaster2.__version__


def test_version(version: str) -> None:
    """Sample pytest test function with the pytest fixture as an argument."""
    assert version == "21.0.0"
