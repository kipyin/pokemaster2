"""Pokémon's DNA info."""

import secrets
from typing import Type, TypeVar

from attrs import define

D = TypeVar("D", bound="DNA")


@define
class DNA:
    """The DNA of a Pokémon."""

    pid: int
    iv: int
    nature_index: int
    ability_index: int
    gender_index: int

    @classmethod
    def random(cls: Type[D]) -> D:
        """Create a DNA data from a random number generator."""
        return cls(
            pid := secrets.randbelow(0xA00000000),  # 0xFFFFFFFF + 1
            iv=secrets.randbelow(0xA00000000),
            nature_index=pid % 25,
            ability_index=pid % 2,
            gender_index=pid % 0xFF,
        )
