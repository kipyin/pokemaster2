"""Load csv files into database."""
import csv
from pathlib import Path
from typing import Optional, Sequence

import peewee
from loguru import logger

from pokemaster2.db import default, tables

# from playhouse import db_url


def get_database(uri: Optional[str] = None) -> peewee.SqliteDatabase:
    """Connect to and return a database."""
    if uri is None:
        uri, origin = default.db_uri_with_origin()
    # elif not uri.startswith("sqlite://")
    else:
        uri, origin = uri, "command-line"

    # database = db_url.connect(uri)
    database = peewee.SqliteDatabase(uri)
    if database.connect():
        logger.debug(
            "Connected to database {database} (from {origin}).", database=uri, origin=origin
        )
    else:
        logger.error(
            "Failed to connect to database {database} (from {origin}", database=uri, origin=origin
        )

    return database


def get_csv_dir(csv_dir: Optional[str] = None) -> str:
    """Return the csv dir we are about to use."""
    if csv_dir is None:
        csv_dir, origin = default.csv_dir_with_origin()
    else:
        csv_dir, origin = csv_dir, "command-line"

    logger.debug("Using csv directory {csv_dir} (from {origin}).", csv_dir=csv_dir, origin=origin)
    return csv_dir


def load(
    database: peewee.SqliteDatabase,
    csv_dir: str,
    models: Sequence[tables.BaseModel] = None,
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
    # Use all tables if no table is provided.
    models = models or tables.MODELS
    logger.debug("Tables to be loaded: {tables}", tables=models)

    # Load tables faster.
    if not safe:
        database.synchronous = 0
        database.journal_mode = "memory"
        logger.debug(
            "Safe option turned off: synchronous: {sync}, journal-mode: {mode}",
            sync=database.synchronous,
            mode=database.journal_mode,
        )

    logger.debug("Opening database {uri}", uri=database.database)
    with database.atomic():
        logger.debug("Opened database {uri}", uri=database.database)
        # Enable foreign keys
        database.foreign_keys = 1
        logger.debug("Foreign key set to {fk}", fk=database.foreign_keys)

        # Bind the database.
        database.bind(models, bind_refs=recursive, bind_backrefs=recursive)
        logger.debug("Bound database.")

        # Drop tables if asked.
        if drop_tables:
            database.drop_tables(models)
            logger.debug("Dropped tables: {tables}", tables=models)

        # Create tables.
        database.create_tables(models)
        logger.debug("Tables created.")

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

                logger.debug("Written table {table} into database.", table=model._meta.table_name)

            except IOError:
                # Log the error and continue the next loop.
                logger.error("CSV file not found: {csv_file}", csv_file=csv_file_path.name)
                continue

    return True
