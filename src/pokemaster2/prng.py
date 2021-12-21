"""Provides the pseudo-random number generator used in various places."""
from typing import Generator, List, Tuple, TypeVar

import attr

P = TypeVar("P", bound="PRNG")


@attr.s(slots=True, auto_attribs=True, cmp=False)
class PRNG:
    """A linear congruential random number generator.

    Usage:
        >>> prng = PRNG()
        >>> prng()
        0
        >>> prng()
        59774

    References:
        https://bulbapedia.bulbagarden.net/wiki/Pseudorandom_number_generation_in_Pokémon
        https://www.smogon.com/ingame/rng/pid_iv_creation#pokemon_random_number_generator
    """

    seed: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    _gen: int = attr.ib(validator=attr.validators.in_(range(1, 8)), default=3)
    _initial_seed: int = attr.ib(init=False)

    def __attrs_post_init__(self: P) -> None:
        """Record the initial seed right after instantiation."""
        self._initial_seed = self.seed

    def _generator(self: P) -> Generator:
        if self._gen == 3:
            while True:
                self.seed = (0x41C64E6D * self.seed + 0x6073) & 0xFFFFFFFF
                yield self.seed >> 16
        else:
            raise ValueError(f"Gen. {self._gen} PRNG is not supported yet.")

    def __call__(self: P) -> int:
        """Move to the next random number."""
        try:
            return next(self._generator())
        except StopIteration:
            self.reset()
            return next(self._generator())

    def reset(self: P) -> None:
        """Reset the generator with the initial seed."""
        self.seed = self._initial_seed

    def next_(self: P, n: int) -> List[int]:
        """Generate the next n random numbers."""
        return [self() for _ in range(n)]

    def generate_pid_and_iv(self: P, method: int = 2) -> Tuple[int, int]:
        """Generate the PID and IVs using the internal generator.

        The generated 32-bit IVs is different from how it is actually
        stored.

        Method 1: [PID] [PID] [IVs] [IVs]
        Method 2: [PID] [PID] [xxxx] [IVs] [IVs]
        Method 4: [PID] [PID] [IVs] [xxxx] [IVs]

        Methods 2 and 4 are only used in Pokemon Ruby, Sapphire, Emerald,
        Fire Red and Leaf Green (RSEFRLG) to produce wild Pokemon.

        All the Pokemon you catch in these games that are not wild Pokemon
        are created using Method 1.

        The criterion for choosing whether to use Method 1, 2, or 4 in the
        creation of wild Pokemon in RSEFRLG seems to be arbitrary.

        Checkout [this link](https://www.smogon.com/ingame/rng/pid_iv_creation#rng_pokemon_generation)  # noqa: E501
        for more information on Method 1, 2, and 4.

        Args:
            method: 1, 2, or 4.

        Raises:
            ValueError: if the method is not in (1, 2, 4).

        Returns:
            a tuple of two integers, in the order of 'PID' and 'IVs'.
        """
        if method not in (1, 2, 4):
            raise ValueError(
                "Only methods 1, 2, 4 are supported. For more information on "
                "the meaning of the methods, see "
                "https://www.smogon.com/ingame/rng/pid_iv_creation#rng_pokemon_generation"
                " for help."
            )

        return self._generate_pid(), self._generate_iv(method)

    def _generate_pid(self: P) -> int:
        """Create the Personality ID (PID) for a Pokémon.

        Returns:
            int
        """
        pid_src_1, pid_src_2 = self.next_(2)
        return pid_src_1 + (pid_src_2 << 16)

    def _generate_iv(self: P, method: int = 2) -> int:
        """Create the number used to generate a Pokémon's IVs.

        Args:
            method: the Pokémon generation method. Valid values are 1, 2, and 4.

        Returns:
            int
        """
        if method == 1:
            iv_src_1, iv_src_2 = self.next_(2)
        elif method == 2:
            _, iv_src_1, iv_src_2 = self.next_(3)
        else:  # method == 4:
            iv_src_1, _, iv_src_2 = self.next_(3)

        return iv_src_1 + (iv_src_2 << 16)

    def random(self: P) -> float:
        """Generate a random number from the uniform distribution [0, 1).

        Returns:
            A random number between 0 and 1.
        """
        return self() / 0x10000
