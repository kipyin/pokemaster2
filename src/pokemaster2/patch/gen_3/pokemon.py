"""Generation 3 Pokémon."""
from typing import Optional, Type, TypeVar

from attrs import define

from pokemaster2.base_pokemon import BasePokemon
from pokemaster2.db import get
from pokemaster2.prng import PRNG
from pokemaster2.stats import Stats

# from pokemaster2.stats import Stats

P = TypeVar("P", bound="Generation3Pokemon")


prng = PRNG()


@define
class Generation3Pokemon(BasePokemon):
    """Generation 3 Pokémon."""

    @classmethod
    def from_pokedex(
        cls: Type[P],
        # database: peewee.SqliteDatabase,
        national_id: Optional[int] = None,
        species: Optional[str] = None,
        language: Optional[str] = None,
        form: Optional[str] = None,
        level: Optional[int] = None,
        exp: Optional[int] = None,
        item_held: Optional[str] = None,
        pid: Optional[int] = None,
        iv: Optional[Stats] = None,
        ev: Optional[Stats] = None,
    ) -> P:
        """Create a generation-3 Pokémon from the pokedex data with sensible defaults."""
        language = language or get.DEFAULT_LANGUAGE

        # Determine the pokemon's species and form.
        if national_id:
            pokemon = get.pokemon(national_id)
            species = species or pokemon.identifier
        elif species:
            pokemon = get.pokemon(species)
            national_id = national_id or pokemon.species_id
        else:
            raise ValueError("Must specify the Pokémon's id or identifier.")
        pokemon_id = pokemon.id  # FIXME: this pokemon is of the default form!

        # Set the level and experience.
        if level and exp is None:
            exp = get.minimum_experience(pokemon_id=national_id, level=level)
        elif exp and level is None:
            NotImplemented
        elif level is None and exp is None:
            raise ValueError("Must specify the Pokémon's level or exp.")
        else:
            # both level and exp are set, no modification needed.
            pass

        # Determine the Pokémon's personality value and IV.
        if pid is None:
            pid, iv_gene = prng.generate_pid_and_iv(method=2)
        else:
            _, iv_gene = prng.generate_pid_and_iv(method=2)

        # Set IV and EV.
        iv = iv or Stats.create_iv(gene=iv_gene)
        ev = ev or Stats.zeros()

        # Calculate the stats.
        base_stats, ev_yields = get.base_stats_and_ev_yields(species_id=national_id, form=form)

        stats = Stats.calc(level=level, base_stats=base_stats, iv=iv, ev=ev, nature="")
        current_stats = stats

        return cls(
            national_id=national_id,
            species=species,
            form=form,
            types=get.pokemon_types(pokemon_id=pokemon_id),
            level=level,
            exp=exp,
            item_held=item_held,
            base_stats=base_stats,
            pid=pid,
            iv=iv,
            ev=ev,
            stats=stats,
            current_stats=current_stats,
        )
