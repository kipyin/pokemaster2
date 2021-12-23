"""Base Pokemon."""
from typing import Mapping, Sequence, TypeVar, Union

import attr

from pokemaster2.stats import Stats

P = TypeVar("P", bound="BasePokemon")


@attr.s(auto_attribs=True)
class BasePokemon:
    """The underlying structure of a Pokémon.

    No fancy initializations, no consistency checks, just a very basic
    Pokémon model. Anything is possible with this BasePokemon. This
    class also contains common and basic behaviors of Pokémon, such as
    leveling-up, learning/forgetting moves, evolving into another
    Pokémon, etc.

    This class is never meant to be instantiated directly.
    """

    national_id: int
    species: str
    types: Sequence[str]
    item_held: str
    exp: int
    level: int

    base_stats: Stats
    iv: Stats
    current_stats: Stats
    stats: Stats
    ev: Stats

    move_set = Mapping[int, Mapping[str, Union[str, int]]]
    pid: str
    gender: str
    nature: str
    ability: str

    # def evolve(self: P) -> None:
    #     """
    #     Evolve into another Pokémon.

    #     1. Statistics are updated.
    #     2. Learnset is updated.
    #     3. Evolution tree is updated.

    #     Returns:
    #         Nothing

    #     """
    #     pass

    def level_up(self: P) -> Stats:
        """Increase `Pokemon`'s level by 1.

        All stats are bumped accordingly.

        Returns:
            Stats: how much the stats has been increased.
        """
        # Increment the level
        self.level += 1

        # Calculate the new stats after the level increment.
        new_stats = Stats.calc(
            level=self.level,
            base_stats=self.base_stats,
            iv=self.iv,
            ev=self.ev,
            nature=self.nature,
        )

        # Get the difference between the old stats and the new.
        stats_diff = new_stats - self.stats

        # In the case when the current hp is not full, the hp will be bumped proportionally.
        current_hp_proportion = self.current_stats.hp / self.stats.hp

        # Set the permanent stats and the current stats to the newly calculated stats.
        self.stats = new_stats
        self.current_stats = new_stats

        # Adjust the current hp so that the relative proportion of the current / permanent
        # stays the same.
        self.current_stats.hp = int(new_stats.hp * current_hp_proportion)

        return stats_diff

    # @classmethod
    # def blank_from_pokedex(
    #     cls: "BasePokemon",
    #     national_id: int,
    #     level: int,
    #     item_held: str = None,
    #     iv: Stats = None,
    #     ev: Stats = None,
    #     pid: int = None,
    #     nature: str = None,
    #     ability: str = None,
    #     gender: str = None,
    # ) -> "BasePokemon":
    #     """Instantiate a `BasePokemon` by its national id.

    #     Everything else is randomized.

    #     Args:
    #         national_id: the Pokemon's ID in the National Pokedex.
    #         level: Pokemon's level.
    #         item_held: Pokemon's holding item.
    #         iv: Pokemon's individual values, `Stats`, used to determine its permanent stats.
    #             A random IV will be set if not provided.
    #         ev: Pokemon's effort values, `Stats`, used to determine its permanent stats. An
    #             all-zero ev will be set if not provided.
    #         pid: Pokemon's personality id. `nature`, `ability`, and `gender` will use
    #             their provided value first. A random `pid` will be set if not provided.
    #         nature: Pokemon's nature, used to determine its permanent stats. If nothing is
    #             provided, then the function will use `pid` to determine its `nature`.
    #         ability: Pokemon's ability, `str`. If nothing is provided, then the function
    #             will use `pid` to determine its `nature`.
    #         gender: Pokemon's gender.  If nothing is provided, then the function will use
    #             `pid` to determine its `nature`.

    #     Returns:
    #         A `BasePokemon` instance.
    #     """
    #     # Build pokemon data
    #     pokemon_data = get.pokemon(pokemon_id=national_id)
    #     growth_data = get.minimum_experience(pokemon_id=national_id, level=level)
    #     species_data = pokemon_data.species
    #     species = species_data.identifier

    #     # Determine stats
    #     gene = prng.create_gene()
    #     iv = iv or Stats.create_iv(gene=gene)
    #     ev = ev or Stats.zeros()
    #     base_stats = {}
    #     for i, stat in enumerate(STAT_NAMES):
    #         base_stats[stat] = pokemon_data.stats[i].base_stat
    #     stats = _calc_stats(level=level, base_stats=base_stats, iv=iv, ev=ev, nature=nature)
    #     current_stats = stats

    #     # PID related attributes
    #     pid = pid or prng.create_personality()
    #     nature = nature
    #     ability = ability
    #     gender = gender

    #     return cls(
    #         pid=pid,
    #         national_id=species_data.id,
    #         species=species,
    #         types=list(map(lambda x: x.identifier, pokemon_data.types)),
    #         item_held=item_held,
    #         exp=growth_data.experience,
    #         level=growth_data.level,
    #         stats=stats,
    #         current_stats=current_stats,
    #         ev=ev,
    #         iv=iv,
    #         nature=nature,
    #         ability=ability,
    #         gender=gender,
    #     )


def _calc_stats(level: int, base_stats: Stats, iv: Stats, ev: Stats, nature: str) -> Stats:
    """Calculate the Pokemon's stats."""
    nature_modifiers = Stats.nature_modifiers(nature)
    residual_stats = Stats(
        hp=10 + level,
        atk=5,
        def_=5,
        spatk=5,
        spdef=5,
        spd=5,
    )

    stats = ((base_stats * 2 + iv + ev // 4) * level // 100 + residual_stats) * nature_modifiers
    if base_stats.hp == 1:
        stats.hp = 1
    return stats
