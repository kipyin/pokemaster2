"""Database queries."""
from typing import Dict, List, Tuple, Union

import peewee
from loguru import logger

from pokemaster2.db import tables as t
from pokemaster2.stats import Stats

DEFAULT_VERSION = "diamond"
DEFAULT_LANGUAGE = "en"


def pokemon_by_id(pokemon_id: int) -> t.Pokemon:
    """Fetch a Pokémon data by id."""
    q = (
        t.Pokemon.select(t.Pokemon)
        .where((t.Pokemon.species == pokemon_id) & (t.Pokemon.is_default == True))  # noqa: E712
        .first()
    )
    return q


def pokemon_by_identifier(identifier: str) -> t.Pokemon:
    """Fetch a Pokémon data by its identifier."""
    q = (
        t.Pokemon.select(t.Pokemon)
        .join(t.PokemonSpecies)
        .where(t.PokemonSpecies.identifier == identifier)
        .first()
    )
    return q


def pokemon(query: Union[int, str]) -> t.Pokemon:
    """Fetch a Pokémon data by id or identifier."""
    if isinstance(query, int):
        return pokemon_by_id(query)
    elif isinstance(query, str):
        return pokemon_by_identifier(query)


def pokedex_entry(
    pokemon_id: int, language: str = DEFAULT_LANGUAGE, version: str = DEFAULT_VERSION
) -> peewee.ModelRaw:
    """Get a pokedex entry."""
    q = t.Pokemon.raw(
        """SELECT p.species_id, name, genus, flavor_text, height, weight
                FROM pokemon p
                JOIN languages l ON l.identifier=?
                JOIN versions v ON v.identifier=?
                JOIN pokemon_species_names s
                    ON s.local_language_id=l.id
                    AND s.pokemon_species_id=p.species_id
                JOIN pokemon_species_flavor_text f
                    ON f.language_id=l.id
                    AND f.version_id=v.id
                    AND f.species_id = p.species_id
                WHERE p.species_id=?""",
        language,
        version,
        pokemon_id,
    )
    return list(q)[0]


def pokemon_name(pokemon_id: int, language: str = DEFAULT_LANGUAGE) -> str:
    """Get a Pokémon's name."""
    q = (
        t.PokemonSpeciesNames.select(t.PokemonSpeciesNames, t.Languages)
        .join(t.Languages, on=(t.Languages.identifier == language))
        .where(
            (t.PokemonSpeciesNames.local_language == t.Languages.id)
            & (t.PokemonSpeciesNames.pokemon_species == pokemon_id)  # noqa: W503
        )
        .first()
    )
    return q.name


def pokemon_types(pokemon_id: int) -> List[t.Types]:
    """Get Pokémon types."""
    q = (
        t.Types.select(t.Types, t.PokemonTypes)
        .join(t.PokemonTypes)
        .where(t.PokemonTypes.pokemon == pokemon_id)
    )
    return list(q)


EvolutionStage = Tuple[int, str, int]
EvolutionChain = List[EvolutionStage]
EvolutionTree = Dict[EvolutionStage, "EvolutionTree"]


def pokemon_evolution_chain(pokemon_id: int, language: str = DEFAULT_LANGUAGE) -> EvolutionTree:
    """Get Pokémon evolution chain."""
    # First locate the PokemonSpecies' evolution chain.
    evolution_chain_id = (
        t.PokemonSpecies.select()
        .where(t.PokemonSpecies.id == pokemon_id)
        .first()
        .evolution_chain_id
    )
    logger.debug("Evolution chain ID: {c}", c=evolution_chain_id)

    # Find all PokemonSpecies in the same evolution chain.
    q = t.PokemonSpecies.select(t.PokemonSpecies.id, t.PokemonSpecies.evolves_from_species).where(
        t.PokemonSpecies.evolution_chain == evolution_chain_id
    )
    logger.debug("Query result: {q}", q=list(q))

    # `chain` is a list of
    # Tuple[PokemonSpecies.id, PokemonSpecise.name, PokemonSpecies.evolves_from_species_id]
    chain: EvolutionChain = [
        (row.id, pokemon_name(row.id, language), row.evolves_from_species_id) for row in q
    ]
    logger.debug("Chain: {chain}", chain=chain)

    # `root` is the part of the chain whose `evolves_from_species_id` is None.
    try:
        root: EvolutionStage = next((pkmn for pkmn in chain if pkmn[2] is None))
    except StopIteration:
        root = chain[0]
    logger.debug("Root: {root}", root=root)

    # `tree` is a recursive dict, such as
    # {(1, 'Bulbasaur', None): {(2, 'Ivysaur', 1): {(3, 'Venusaur', 2): {}}}}
    tree: EvolutionTree = {root: {}}

    del chain[chain.index(root)]
    logger.debug("Chain after deleting root: {c}", c=chain)

    def add_evolutions(tree: EvolutionTree, root: EvolutionStage, chain: EvolutionChain) -> None:
        """Add evolutions to `tree` recursively."""
        evolutions = [pkmn for pkmn in chain if pkmn[2] == root[0]]
        for evolution in evolutions:
            tree[root][evolution] = {}
            del chain[chain.index(evolution)]
            add_evolutions(tree[root], evolution, chain)

    add_evolutions(tree, root, chain)

    return tree


def minimum_experience(pokemon_id: int, level: int) -> int:
    """Get the minimum experience of a Pokémon at a certain level."""
    growth_rate_id = (
        t.PokemonSpecies.select(t.PokemonSpecies.growth_rate)
        .where(t.PokemonSpecies.id == pokemon_id)
        .first()
    )
    experience = (
        t.Experience.select(t.Experience.experience)
        .where((t.Experience.growth_rate == growth_rate_id) & (t.Experience.level == level))
        .first()
    )
    return experience


def abilities(pokemon_id: int) -> List[t.Ability]:
    """Get all abilities of a Pokémon."""


def base_stats(species_id: int, form_: str) -> Stats:
    """Fetch and return a `Stats` instance of the Pokémon's base stats."""


def forms(species_id: int, language: str = DEFAULT_LANGUAGE) -> List[t.PokemonForms]:
    """Fetch all of a Pokémon's forms.

    Args:
        species_id: int, the species' national id.
        language: str, the language of the forms' names.

    Returns:
        List[t.PokemonForms]: a list of PokemonForms.
    """
    # First get all pokemon under the same species id
    pokemon_with_same_id = (
        t.Pokemon.select(t.Pokemon.id)
        .join(t.PokemonSpecies)
        .where(t.PokemonSpecies.id == species_id)
    )
    q = (
        t.PokemonForms.select(t.PokemonForms, t.PokemonFormNames, t.Languages)
        .join(t.PokemonFormNames)
        .join(t.Languages, on=(t.Languages.identifier == language))
        .where(
            (t.PokemonForms.pokemon_id.in_(pokemon_with_same_id))
            & (t.PokemonFormNames.local_language == t.Languages.id)  # noqa: W503
        )
    )
    return list(q)
