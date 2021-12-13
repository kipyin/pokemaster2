"""Tests for `pokemaster2`.cli module."""
from typing import List

import pytest
from click.testing import CliRunner

import pokemaster2
from pokemaster2 import cli


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "pokemaster2.cli.main"),
        (["--help"], "Usage: main [OPTIONS]"),
        (["--version"], f"main, version { pokemaster2.__version__ }\n"),
    ],
)
def test_command_line_interface(options: List[str], expected: str) -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, options)
    assert result.exit_code == 0
    assert expected in result.output
