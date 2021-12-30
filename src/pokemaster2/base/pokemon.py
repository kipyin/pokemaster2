"""Base Pokemon."""
from typing import Mapping, Sequence, TypeVar, Union

from attrs import define

from pokemaster2.base.stats import Stats

P = TypeVar("P", bound="BasePokemon")


@define
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
    form: str
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
    pid: int
    gender: str
    nature: str
    ability: str

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
