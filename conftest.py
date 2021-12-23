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


POKEMON_COLUMN_NAMES = [
    "id",
    "identifier",
    "species_id",
    "height",
    "weight",
    "base_experience",
    "order",
    "is_default",
]
SPECIES_COLUMN_NAMES = [
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
SPECIES_NAME_COLUMN_NAME = ["pokemon_species_id", "local_language_id", "name", "genus"]


@pytest.fixture(scope="function")
def bulbasaur(empty_db) -> t.Pokemon:
    """Create a bulbasaur instance of `Pokemon`."""
    data = [1, "bulbasaur", 1, 7, 69, 64, 1, 1]
    q = t.Pokemon.create(**dict(zip(POKEMON_COLUMN_NAMES, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def bulbasaur_species(empty_db) -> t.PokemonSpecies:
    """Create a bulbasaur species instance of `PokemonSpecies`."""
    data = [1, "bulbasaur", 1, None, 1, 5, 8, 3, 1, 45, 50, 0, 20, 0, 4, 0, 0, 0, 1, None]
    q = t.PokemonSpecies.create(**dict(zip(SPECIES_COLUMN_NAMES, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def ivysaur_species(empty_db) -> t.PokemonSpecies:
    """Create a bulbasaur species instance of `PokemonSpecies`."""
    data = [2, "ivysaur", 1, 1, 1, 5, 8, 3, 1, 45, 50, 0, 20, 0, 4, 0, 0, 0, 2, None]
    q = t.PokemonSpecies.create(**dict(zip(SPECIES_COLUMN_NAMES, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def venusaur_species(empty_db) -> t.PokemonSpecies:
    """Create a bulbasaur species instance of `PokemonSpecies`."""
    data = [3, "venusaur", 1, 2, 1, 5, 8, 3, 1, 45, 50, 0, 20, 1, 4, 1, 0, 0, 3, None]
    q = t.PokemonSpecies.create(**dict(zip(SPECIES_COLUMN_NAMES, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def bulbasaur_name() -> t.PokemonSpeciesNames:
    """Test data for `PokemonSpeciesNames`."""
    data = [1, 9, "Bulbasaur", "Seed Pokémon"]
    q = t.PokemonSpeciesNames.create(**dict(zip(SPECIES_NAME_COLUMN_NAME, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def ivysaur_name() -> t.PokemonSpeciesNames:
    """Test data for `PokemonSpeciesNames`."""
    data = [2, 9, "Ivysaur", "Seed Pokémon"]
    q = t.PokemonSpeciesNames.create(**dict(zip(SPECIES_NAME_COLUMN_NAME, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def venusaur_name() -> t.PokemonSpeciesNames:
    """Test data for `PokemonSpeciesNames`."""
    data = [3, 9, "Venusaur", "Seed Pokémon"]
    q = t.PokemonSpeciesNames.create(**dict(zip(SPECIES_NAME_COLUMN_NAME, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def bulbasaur_evolution_chain() -> t.EvolutionChains:
    """Create a test instance of `EvolutionChains`."""
    EVOLUTION_CHAIN_COLUMN = ["id", "baby_trigger_item_id"]
    data = [1, None]
    q = t.EvolutionChains.create(**dict(zip(EVOLUTION_CHAIN_COLUMN, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def growth_medium_slow(empty_db) -> t.GrowthRates:
    """Create a medium-slow GrowthRate instance."""
    column_names = ["id", "identifier", "formula"]
    data = [4, "medium-slow", r"\frac{6x^3}{5} - 15x^2 + 100x - 140"]
    q = t.GrowthRates.create(**dict(zip(column_names, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def language_english() -> t.Languages:
    """Test data for `Languages`."""
    LANGUAGE_COLUMNS = ["id", "iso639", "iso3166", "identifier", "official", "order"]
    data = [9, "en", "us", "en", 1, 7]
    q = t.Languages.create(**dict(zip(LANGUAGE_COLUMNS, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def version_red() -> t.Versions:
    """Test data for `Versions`."""
    VERSION_COLUMN = ["id", "version_group_id", "identifier"]
    data = [1, 1, "red"]
    q = t.Versions.create(**dict(zip(VERSION_COLUMN, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def bulbasaur_flavor_text() -> t.PokemonSpeciesFlavorText:
    """Test data for `PokemonSpeciesFlavorText`."""
    POKEMON_SPECIES_FLAVOR_TEXT_COLUMN = ["species_id", "version_id", "language_id", "flavor_text"]
    data = [
        1,
        1,
        9,
        "A strange seed was\nplanted on its\nback at birth.The plant sprouts"
        "\nand grows with\nthis POKéMON.",
    ]
    q = t.PokemonSpeciesFlavorText.create(**dict(zip(POKEMON_SPECIES_FLAVOR_TEXT_COLUMN, data)))
    yield q
    q.delete_instance()


@pytest.fixture(scope="function")
def bulbasaur_types() -> None:
    """Test data for `PokemonTypes`."""
    # POKEMON_TYPE_COLUMN = ["pokemon_id", "type_id", "slot"]
    data = [
        [1, 12, 1],
        [1, 4, 2],
    ]
    q = t.PokemonTypes.insert_many(
        data, fields=[t.PokemonTypes.pokemon, t.PokemonTypes.type, t.PokemonTypes.slot]
    ).execute()
    yield q
    t.PokemonTypes.delete()


@pytest.fixture(scope="function")
def types():
    """Test data for `Types`."""
    # TYPES_COLUMNS = ["id", "identifier", "generation_id", "damage_class_id"]
    data = [
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
    q = t.Types.insert_many(
        data, fields=[t.Types.id, t.Types.identifier, t.Types.generation, t.Types.damage_class]
    ).execute()
    yield q
    t.Types.delete()
