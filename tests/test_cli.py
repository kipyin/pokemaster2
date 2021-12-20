"""Tests for `pokemaster2`.cli module."""
from typing import List

import pytest
from click.testing import CliRunner

import pokemaster2
from pokemaster2 import cli


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "Console script for pokemaster2"),
        (["--help"], "Usage: main [OPTIONS] COMMAND [ARGS]..."),
        (["--version"], f"main, version { pokemaster2.__version__ }\n"),
        (["load"], ""),
    ],
)
def test_command_line_interface(options: List[str], expected: str, test_csv_dir) -> None:
    """Test the CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem(test_csv_dir.parent.parent):  # src dir
        result = runner.invoke(cli.main, options)
        assert result.exit_code == 0
        assert expected in result.output
