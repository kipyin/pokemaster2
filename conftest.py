"""Pytest fixtures."""

import peewee
import pytest

from pokemaster2.db.tables import MODELS, GrowthRates, Pokemon, PokemonSpecies


@pytest.fixture(autouse=True)
def empty_db():
    """Create, connect, and yield an empty database. Close after use."""
    db = peewee.SqliteDatabase(":memory:")
    db.bind(MODELS, bind_refs=True, bind_backrefs=True)
    db.connect()
    db.create_tables(MODELS)
    yield db
    db.drop_tables(MODELS)
    db.close()


@pytest.fixture
def bulbasaur():
    """Create a bulbasaur instance of `Pokemon`."""
    column_names = [
        "id",
        "identifier",
        "species_id",
        "height",
        "weight",
        "base_experience",
        "order",
        "is_default",
    ]
    data = [1, "bulbasaur", 1, 7, 69, 64, 1, 1]
    yield Pokemon.create(**dict(zip(column_names, data)))


@pytest.fixture
def bulbasaur_species():
    """Create a bulbasaur species instance of `PokemonSpecies`."""
    column_names = [
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
        "order",
        "conquest_order",
    ]
    data = [1, "bulbasaur", 1, None, 1, 5, 8, 3, 1, 45, 70, 0, 20, 0, 4, 0, 1]
    yield PokemonSpecies.create(**dict(zip(column_names, data)))


@pytest.fixture
def test_pokemon_species():
    test_pokemon_species = PokemonSpecies.create(
        id=1,
        identifier="test-species",
        generation_id=1,
        evolves_from_species_id=None,
        evolution_chain_id=1,
        color_id=1,
        shape_id=1,
        habitat_id=1,
        gender_rate=8,
        capture_rate=255,
        base_happiness=0,
        is_baby=False,
        hatch_counter=10,
        has_gender_differences=False,
        growth_rate_id=1,
        forms_switchable=False,
        order=1,
        conquest_order=1,
    )
    yield test_pokemon_species


@pytest.fixture
def test_pokemon():
    yield Pokemon.create(
        id=1,
        identifier="test-pokemon",
        species_id=1,
        height=10,
        weight=10,
        base_experience=100,
        order=1,
        is_default=True,
    )


@pytest.fixture
def test_growth_rate():
    yield GrowthRates.create(
        id=1,
        identifier="test-growth",
        formula="test-growth-formula",
    )


@pytest.fixture(scope="session")
def test_csv_dir(tmp_path_factory):
    """Create a temp path for `data/csv`."""
    csv_dir = tmp_path_factory.mktemp("data", numbered=False) / "csv"
    csv_dir.mkdir()
    yield csv_dir


@pytest.fixture(scope="function")
def test_pokemon_csv(test_csv_dir):
    """Create a temp pokemon CSV file in `data/csv/`."""
    content = """id,identifier,species_id,height,weight,base_experience,order,is_default
1,bulbasaur,1,7,69,64,1,1
"""
    pokemon_csv = test_csv_dir / "pokemon.csv"
    pokemon_csv.write_text(content)
    yield pokemon_csv
