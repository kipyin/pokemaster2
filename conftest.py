"""Pytest fixtures."""

import peewee
import pytest

from pokemaster2.db.tables import MODELS, GrowthRates, Pokemon, PokemonSpecies


@pytest.fixture
def test_db():
    db = peewee.SqliteDatabase(":memory:")
    db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables(MODELS)
    yield db
    db.drop_tables(MODELS)
    db.close()


@pytest.fixture
def test_pokemon_species():
    test_pokemon_species = PokemonSpecies.create(
        id=1,
        identifier="test-species",
        evolves_from=None,
        gender_rate=8,
        capture_rate=255,
        base_happiness=0,
        is_baby=False,
        hatch_counter=10,
        has_gender_differences=False,
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
