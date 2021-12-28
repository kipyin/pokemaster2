"""Pytest fixtures."""
import peewee
import pytest

from pokemaster2.db import tables as t

TEST_MODELS = [
    t.EvolutionChains,
    t.GrowthRates,
    t.Pokemon,
    t.PokemonSpecies,
    t.PokemonSpeciesNames,
    t.PokemonSpeciesFlavorText,
    t.Languages,
    t.Versions,
    t.PokemonTypes,
    t.Types,
]


# === Table fields ===

POKEMON_FIELDS = [
    "id",
    "identifier",
    "species_id",
    "height",
    "weight",
    "base_experience",
    "order",
    "is_default",
]
POKEMON_SPECIES_FIELDS = [
    "id",
    "identifier",
    "generation_id",
    "evolves_from_species_id",
    "evolution_chain_id",
    "color_id",
    "shape_id",
    "habitat_id",
    "gender_rate",
    "capture_rate",
    "base_happiness",
    "is_baby",
    "hatch_counter",
    "has_gender_differences",
    "growth_rate_id",
    "forms_switchable",
    "is_legendary",
    "is_mythical",
    "order",
    "conquest_order",
]
POKEMON_SPECIES_NAME_FIELDS = ["pokemon_species_id", "local_language_id", "name", "genus"]

GROWTH_RATE_FIELDS = ["id", "identifier", "formula"]

EVOLUTION_CHAIN_FIELDS = ["id", "baby_trigger_item_id"]

LANGUAGE_FIELDS = ["id", "iso639", "iso3166", "identifier", "official", "order"]

VERSION_FIELDS = ["id", "version_group_id", "identifier"]

POKEMON_SPECIES_FLAVOR_TEXT_FIELDS = ["species_id", "version_id", "language_id", "flavor_text"]

POKEMON_TYPES_FIELDS = ["pokemon_id", "type_id", "slot"]

TYPES_FIELDS = ["id", "identifier", "generation_id", "damage_class_id"]

# === Table data ===

POKEMON_DATA = [
    [1, "bulbasaur", 1, 7, 69, 64, 1, 1],
]
POKEMON_SPECIES_DATA = [
    [1, "bulbasaur", 1, None, 1, 5, 8, 3, 1, 45, 50, 0, 20, 0, 4, 0, 0, 0, 1, None],
    [2, "ivysaur", 1, 1, 1, 5, 8, 3, 1, 45, 50, 0, 20, 0, 4, 0, 0, 0, 2, None],
    [3, "venusaur", 1, 2, 1, 5, 8, 3, 1, 45, 50, 0, 20, 1, 4, 1, 0, 0, 3, None],
]
POKEMON_SPECIES_NAME_DATA = [
    [1, 9, "Bulbasaur", "Seed Pokémon"],
    [2, 9, "Ivysaur", "Seed Pokémon"],
    [3, 9, "Venusaur", "Seed Pokémon"],
]
GROWTH_RATE_DATA = [
    [4, "medium-slow", r"\frac{6x^3}{5} - 15x^2 + 100x - 140"],
]
EVOLUTION_CHAIN_DATA = [1, None]

LANGUAGE_DATA = [
    [9, "en", "us", "en", 1, 7],
]
VERSION_DATA = [
    [1, 1, "red"],
]
POKEMON_SPECIES_FLAVOR_TEXT_DATA = [
    [
        1,
        1,
        9,
        "A strange seed was\nplanted on its\nback at birth.The plant sprouts"
        "\nand grows with\nthis POKéMON.",
    ],
]
POKEMON_TYPES_DATA = [
    [1, 12, 1],
    [1, 4, 2],
]
TYPES_DATA = [
    [1, "normal", 1, 2],
    [2, "fighting", 1, 2],
    [3, "flying", 1, 2],
    [4, "poison", 1, 2],
    [5, "ground", 1, 2],
    [6, "rock", 1, 2],
    [7, "bug", 1, 2],
    [8, "ghost", 1, 2],
    [9, "steel", 2, 2],
    [10, "fire", 1, 3],
    [11, "water", 1, 3],
    [12, "grass", 1, 3],
    [13, "electric", 1, 3],
    [14, "psychic", 1, 3],
    [15, "ice", 1, 3],
    [16, "dragon", 1, 3],
    [17, "dark", 2, 3],
    [18, "fairy", 6],
]


# === Database Setup ===


@pytest.fixture()
def empty_db():
    """Create, connect, and yield an empty database. Close after use."""
    db = peewee.SqliteDatabase(":memory:")
    db.bind(TEST_MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables(TEST_MODELS)
    yield db
    db.drop_tables(TEST_MODELS)
    db.close()


# === Plumb the data ===


def _insert_data(table: t.BaseModel, data, fields) -> None:
    """Execute `insert_many` commands."""
    table.insert_many(data, fields=fields).execute()


@pytest.fixture
def pokemon_data():
    """Create data for `t.Pokemon`."""
    _insert_data(t.Pokemon, POKEMON_DATA, POKEMON_FIELDS)
    yield


@pytest.fixture
def pokemon_species_data():
    """Create data for `t.PokemonSpecies`."""
    _insert_data(t.PokemonSpecies, POKEMON_SPECIES_DATA, POKEMON_SPECIES_FIELDS)
    yield


@pytest.fixture
def pokemon_species_name_data():
    """Create data for `t.PokemonSpeciesNames`."""
    _insert_data(t.PokemonSpeciesNames, POKEMON_SPECIES_NAME_DATA, POKEMON_SPECIES_NAME_FIELDS)
    yield


@pytest.fixture
def growth_rates_data():
    """Create data for `t.GrowthRates`."""
    _insert_data(t.GrowthRates, GROWTH_RATE_DATA, GROWTH_RATE_FIELDS)
    yield


@pytest.fixture
def evolution_chain_data():
    """Create data for `t.EvolutionChains`."""
    _insert_data(t.EvolutionChains, EVOLUTION_CHAIN_DATA, EVOLUTION_CHAIN_FIELDS)
    yield


@pytest.fixture
def language_data():
    """Create data for `t.Language`."""
    _insert_data(t.Languages, LANGUAGE_DATA, LANGUAGE_FIELDS)


@pytest.fixture
def version_data():
    """Create data for `t.Versions`."""
    _insert_data(t.Versions, VERSION_DATA, VERSION_FIELDS)


@pytest.fixture
def pokemon_species_flavor_text_data():
    """Create data for `t.PokemonSpeciesFlavorText`."""
    _insert_data(
        t.PokemonSpeciesFlavorText,
        POKEMON_SPECIES_FLAVOR_TEXT_DATA,
        POKEMON_SPECIES_FLAVOR_TEXT_FIELDS,
    )


@pytest.fixture
def pokemon_types_data():
    """Create data for `t.PokemonTypes`."""
    _insert_data(t.PokemonTypes, POKEMON_TYPES_DATA, POKEMON_TYPES_FIELDS)


@pytest.fixture
def types_data():
    """Create data for `t.Types`."""
    _insert_data(t.Types, TYPES_DATA, TYPES_FIELDS)
