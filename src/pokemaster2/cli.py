"""Console script for pokemaster2."""

import click
from loguru import logger

from pokemaster2 import __version__
from pokemaster2.db import io


@click.group()
@click.version_option(version=__version__)
def main() -> int:
    """Console script for pokemaster2."""
    # click.echo("Replace this message by putting your code into pokemaster2.cli.main")
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


@main.command("load")
@click.option("-C", "--csv-dir", default=None)
@click.option("-U", "--uri", default=None)
@click.option("-D", "--drop-tables", type=bool, default=True)
@click.option("-S", "--safe", type=bool, default=True)
@click.option("-R", "--recursive", type=bool, default=True)
def cli_load(csv_dir: str, uri: str, drop_tables: bool, safe: bool, recursive: bool) -> None:
    """Load Pokédex data into a database from CSV files."""
    logger.info("Running command `load`.")
    io.load(
        database=io.get_database(uri),
        csv_dir=io.get_csv_dir(csv_dir),
        models=None,
        drop_tables=drop_tables,
        safe=safe,
        recursive=recursive,
    )
    logger.debug("Successfully loaded database.")
    return 0


if __name__ == "__main__":
    main()  # pragma: no cover
