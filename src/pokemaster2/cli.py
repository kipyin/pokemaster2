"""Console script for pokemaster2."""

import click
from loguru import logger

from pokemaster2 import __version__
from pokemaster2.db import io, tables
from pokemaster2.dex import formats
from pokemaster2.dex._pokemon import Pokemon


@click.group()
@click.version_option(version=__version__)
def pmdex() -> int:
    """Console script for pokemaster2."""
    # click.echo("Replace this message by putting your code into pokemaster2.cli.main")
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


@pmdex.command("load")
@click.option("-C", "--csv-dir", default=None)
@click.option("-U", "--uri", default=None)
@click.option("-D", "--drop-tables", type=bool, default=True)
@click.option("-S", "--safe", type=bool, default=True)
@click.option("-R", "--recursive", type=bool, default=True)
def cli_load(csv_dir: str, uri: str, drop_tables: bool, safe: bool, recursive: bool) -> None:
    """Load Pokédex data into a database from CSV files."""
    logger.info("Running command `load`.")

    db_uri = io.get_database(uri)
    logger.debug("Database URI to use: {uri}", uri=db_uri)

    csv_dir_to_use = io.get_csv_dir(csv_dir)
    logger.debug("CSV dir to use: {csv}", csv=csv_dir_to_use)

    io.load(
        database=db_uri,
        csv_dir=csv_dir_to_use,
        models=None,
        drop_tables=drop_tables,
        safe=safe,
        recursive=recursive,
    )
    logger.debug("Successfully loaded database.")
    return 0


@pmdex.command("lookup")
@click.argument("pokemon")
@click.option("-s", "--shiny", is_flag=True, help="Show shiny version of the Pokémon.")
@click.option("-m", "--mega", is_flag=True, help="Show Mega Evolution(s) if available.")
@click.option(
    "-l", "--language", metavar="LANGUAGE", default="en", help="Pokédex language to use."
)
@click.option(
    "-pv", "--pokedex-version", metavar="VERSION", default="x", help="Pokédex version to use."
)
@click.option(
    "-f",
    "--format",
    metavar="FORMAT",
    default="card",
    type=click.Choice(formats.format_names),
    help="Output format (can be %s)." % ", ".join(formats.format_names),
)
def cli_lookup(pokemon, shiny, mega, language, pokedex_version, format):
    """Search a Pokémon and return a Pokédex entry."""
    db = io.get_database()
    db.bind(tables.MODELS, bind_refs=True, bind_backrefs=True)
    with db.atomic():
        pkmn = Pokemon(pokemon, language=language, version=pokedex_version)
        if format == "card":
            formats.card(pkmn, shiny=shiny, mega=mega)
        elif format == "page":
            pass
        else:
            getattr(formats, format)(pkmn)


if __name__ == "__main__":
    pmdex()  # pragma: no cover
