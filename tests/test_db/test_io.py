"""Tests for `pokemaseter2.io`."""
import pytest

from pokemaster2.db import io, tables


@pytest.mark.skip("Fixtures need to be refactored.")
def test_load_unsafe(empty_db, test_csv_dir):
    """Load db with `unsafe=True`."""
    io.load(empty_db, models=[tables.Pokemon], csv_dir=test_csv_dir, safe=False)
    assert 0 == empty_db.synchronous
    assert "memory" == empty_db.journal_mode


@pytest.mark.skip("Fixtures need to be refactored.")
def test_load_drop_table(empty_db, test_csv_dir, test_pokemon_csv):
    """Drop tables."""
    # Load the pokemon table first
    io.load(empty_db, models=[tables.Pokemon], csv_dir=test_csv_dir)
    bulbasaur_1 = tables.Pokemon.select().where(tables.Pokemon.identifier == "bulbasaur").first()
    assert "bulbasaur" == bulbasaur_1.identifier

    # Drop the original pokemon table and load another table
    content = """id,identifier,species_id,height,weight,base_experience,order,is_default
1,bulbasaur_2,1,7,69,64,1,1
"""
    pokemon_csv = test_csv_dir / "pokemon.csv"
    pokemon_csv.write_text(content)
    io.load(empty_db, models=[tables.Pokemon], csv_dir=test_csv_dir, drop_tables=True)
    bulbasaur_2 = tables.Pokemon.select().where(tables.Pokemon.identifier == "bulbasaur_2").first()
    assert "bulbasaur_2" == bulbasaur_2.identifier


@pytest.mark.skip("Fixtures need to be refactored.")
def test_load_pokemon(empty_db, test_pokemon_csv, test_csv_dir):
    """Load Pokemon."""
    io.load(empty_db, models=[tables.Pokemon], csv_dir=test_csv_dir, drop_tables=True)
    bulbasaur = tables.Pokemon.select().where(tables.Pokemon.identifier == "bulbasaur").first()
    assert 1 == bulbasaur.id
