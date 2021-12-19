"""Load csv files into database."""
import csv
from pathlib import Path
from typing import Optional, Sequence

import peewee
from loguru import logger

from pokemaster2.db import default, tables


def load(
    database: peewee.SqliteDatabase,
    models: Sequence[tables.BaseModel] = None,
    csv_dir: Optional[str] = None,
    drop_tables: bool = False,
    safe: bool = True,
    recursive: bool = True,
    # langs: Optional[str] = None,
) -> None:
    """Load data from CSV files into the given database.

    Args:
        database: `peewee` database to use.
        models: List of tables to load. If omitted, all tables are loaded.
        csv_dir: Directory the CSV files reside in.
        drop_tables: Existing tables will be dropped if True.
        safe: Load can be faster if set to False, but can corrupt the db
            if it crashes / interrupted.
        recursive: Load all dependent tables if set to True.

    Returns:
        Nothing.

    """
    # If csv_dir is not provided, get the default dir.
    csv_dir = csv_dir or default.csv_dir()

    # Use all tables if no table is provided.
    models = models or tables.MODELS

    # Load tables faster.
    if not safe:
        database.synchronous = 0
        database.journal_mode = "memory"

    with database.atomic():
        # Enable foreign keys
        database.foreign_keys = 1

        # Bind the database.
        database.bind(models, bind_refs=recursive, bind_backrefs=recursive)

        # Drop tables if asked.
        if drop_tables:
            database.drop_tables(models)

        # Create tables.
        # TODO: what if a table already exists?
        database.create_tables(models)

        # Run through the CSV files and load the data.
        for model in models:
            try:
                # Read CSV data.
                csv_file_path = Path(csv_dir) / f"{model._meta.table_name}.csv"
                csv_dict_reader = csv.DictReader(csv_file_path.open(mode="r"))

                # Insert CSV data to table in batches.
                # http://docs.peewee-orm.com/en/latest/peewee/querying.html#inserting-rows-in-batches
                for batch in peewee.chunked(csv_dict_reader, 100):
                    model.insert_many(batch).execute()

            except IOError:
                # Log the error and continue the next loop.
                logger.error("CSV file not found: {csv_file}", csv_file=csv_file_path.name)
                continue

    return None
