
# Pokemaster2


<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/pokemaster2.svg)](https://pypi.python.org/pypi/pokemaster2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pokemaster2.svg)](https://pypi.python.org/pypi/pokemaster2)
[![Tests](https://github.com/kipyin/pokemaster2/workflows/tests/badge.svg)](https://github.com/kipyin/pokemaster2/actions?workflow=tests)
[![Codecov](https://codecov.io/gh/kipyin/pokemaster2/branch/main/graph/badge.svg)](https://codecov.io/gh/kipyin/pokemaster2)
[![Read the Docs](https://readthedocs.org/projects/pokemaster2/badge/)](https://pokemaster2.readthedocs.io/)
[![PyPI - License](https://img.shields.io/pypi/l/pokemaster2.svg)](https://pypi.python.org/pypi/pokemaster2)

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)

</div>


Get Real, Living™ Pokémon in Python

**Product intent:** a **playable text / command-line Pokémon-style game** first (`pokemaster2 play`), on a **UI-agnostic game core** so a later desktop raiser/battler can reuse the same rules—not a Pokédex client alone.

* GitHub repo: <https://github.com/kipyin/pokemaster2.git>
* Documentation: <https://pokemaster2.readthedocs.io>
* Free software: MIT


## Features

Currently, there is not much you can do with `pokemaster` — the playable CLI loop is **not built yet**.

* Dev tool: load Pokémon CSV data into a SQLite database (`pokemaster2 load`)
* Engine seeds: Generation 3 PRNG (PID / IV) and `Stats` helpers
* Planned: `pokemaster2 play` — starter, wild encounter, menu battle, then a short journey; optional desktop shell later on the same core

## Status & continuation

This project last saw feature work around **late 2021** (Pre-Alpha). Roadmap: CLI-first playable loop + portable core (desktop is a second shell, not a rewrite):

* [docs/continuation-plan.md](docs/continuation-plan.md) (中文)

## Quickstart

```bash
poetry install
# Data maintenance only (not the game):
poetry run pokemaster2 load -U ./pokedex.sqlite3
# Planned:
# poetry run pokemaster2 play
```

## Credits

This package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage
