"""The pokedex database models."""
from typing import List

import peewee

database = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    """BaseModel for all pokdex Models."""

    class Meta:
        """All BaseModel uses database."""

        database = database


class Pokemon(BaseModel):
    """A Pokémon.  The core to this whole mess.

    This table defines "Pokémon" the same way the games do: a form with
    different types, moves, or other game-changing properties counts as a
    different Pokémon.  For example, this table contains four rows for Deoxys,
    but only one for Unown.

    Non-default forms have IDs above 10000.
    IDs below 10000 match the species_id column, for convenience.
    """

    id = peewee.IntegerField(primary_key=True)  # noqa: A003
    identifier = peewee.CharField(
        max_length=79,
        help_text="An identifier, including form iff this row corresponds to a single, named form",
    )
    species_id = peewee.IntegerField(
        help_text="ID of the species this Pokémon belongs to",
    )
    height = peewee.IntegerField(
        help_text="The height of the Pokémon, in tenths of a meter (decimeters)",
    )
    weight = peewee.IntegerField(
        help_text="The weight of the Pokémon, in tenths of a kilogram (hectograms)",
    )
    base_experience = peewee.IntegerField(
        help_text="The base EXP gained when defeating this Pokémon",
    )
    order = peewee.IntegerField(
        index=True,
        help_text=(
            "Order for sorting. Almost national order, " "except families are grouped together."
        ),
    )
    is_default = peewee.BooleanField(
        index=True,
        help_text="Set for exactly one pokemon used as the default for each species.",
    )


class PokemonSpecies(BaseModel):
    """A Pokémon species: the standard 1–151.  Or 649.  Whatever.

    ID matches the National Pokédex number of the species.
    """

    id = peewee.IntegerField(primary_key=True)  # noqa: A003
    identifier = peewee.CharField(
        max_length=79,
        help_text="An identifier",
    )
    # generation_id = peewee.ForeignKeyField(
    #     "Generation",
    #     backref="pokemon_species",
    #     help_text="ID of the generation this species first appeared in",
    # )
    evolves_from_species_id = peewee.ForeignKeyField(
        "self",
        backref="evolves_to",
        null=True,
        help_text="The species from which this one evolves",
    )
    # evolution_chain_id = peewee.ForeignKeyField(
    #     "EvolutionChain",
    #     backref="pokemon_species",
    #     help_text="ID of the species' evolution chain (a.k.a. family)",
    # )
    # color_id = peewee.ForeignKeyField(
    #     "PokemonColor",
    #     backref="pokemon_species",
    #     help_text="ID of this Pokémon's Pokédex color, as used for a gimmick search function in the games.",
    # )
    # shape_id = peewee.ForeignKeyField(
    #     "PokemonShape",
    #     backref="pokemon_species",
    #     help_text="ID of this Pokémon's body shape, as used for a gimmick search function in the games.",
    # )
    # habitat_id = peewee.ForeignKeyField(
    #     "PokemonHabitat",
    #     backref="pokemon_species",
    #     null=True,
    #     help_text="ID of this Pokémon's habitat, as used for a gimmick search function in the games.",
    # )
    gender_rate = peewee.IntegerField(
        help_text="The chance of this Pokémon being female, in eighths; or -1 for genderless",
    )
    capture_rate = peewee.IntegerField(help_text="The base capture rate; up to 255")
    base_happiness = peewee.IntegerField(help_text="The tameness when caught by a normal ball")
    is_baby = peewee.BooleanField(
        help_text="True iff the Pokémon is a baby, i.e. a lowest-stage Pokémon that cannot breed but whose evolved form can.",
    )
    hatch_counter = peewee.IntegerField(
        help_text="Initial hatch counter: one must walk 255 × (hatch_counter + 1) steps before this Pokémon's egg hatches, unless utilizing bonuses like Flame Body's",
    )
    has_gender_differences = peewee.BooleanField(
        help_text="Set iff the species exhibits enough sexual dimorphism to have separate sets of sprites in Gen IV and beyond.",
    )
    # growth_rate_id = peewee.ForeignKeyField(
    #     "PokemonGrowthRate",
    #     backref="pokemon_species",
    #     help_text="ID of the growth rate for this family",
    # )
    forms_switchable = peewee.BooleanField(
        help_text="True iff a particular individual of this species can switch between its different forms.",
    )
    order = peewee.IntegerField(
        index=True,
        help_text="The order in which species should be sorted.  Based on National Dex order, except families are grouped together and sorted by stage.",
    )
    conquest_order = peewee.IntegerField(
        null=True,
        index=True,
        help_text="The order in which species should be sorted for Pokémon Conquest-related tables.  Matches gallery order.",
    )


Pokemon.species = peewee.ForeignKeyField(PokemonSpecies)


def get_pokemon(identifier: str) -> List[Pokemon]:
    """Find a single `Pokemon` instance."""
    pokemon_set = (
        Pokemon.select(Pokemon, PokemonSpecies)
        .join(PokemonSpecies, on=(Pokemon.species_id == PokemonSpecies.id))
        .where(Pokemon.identifier == identifier)
    )

    return pokemon_set


MODELS = [Pokemon, PokemonSpecies]
