# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/), where the numbers follow `year.month.minor` convention.

Changes for the upcoming release are housed in
[`news/`](https://github.com/kipyin/pokemaster2/tree/develop/news).


## [Unreleased]

### Pokédex

#### Changed

- CLI entry point has been changed from `pokemaster2` to `pmdex`.

#### Added

- Pokédex query interface, `pmdex lookup` command, powered by `.dex` submodule.
- Latest data from [veekun-pokedex](https://github.com/veekun/pokedex/tree/master/pokedex/data/csv), including sword & shield.


### Pokemon Models

#### Added

- `base_pokemon.BasePokemon.level_up()` method to let the Pokémon level-up.
- `stats.Stats` comes with handy class methods like `stats.Stats.random_base_stats()`.
- A native nature class, `stats.Nature`.
- Generation 3 consistent Pokémon class, `Generation3Pokemon`, inherits from `BasePokemon`.


## [21.12.3] - 2021-12-21
### Fixed
- Readthedocs not being able to find `furo`.


## [21.12.2] - 2021-12-21
### Fixed
- Finalized version schema to `{year}.{month}.{minor}`.
- Fixed docs on readthedocs


## [21.12.1] - 2021-12-21
### Added
- A very primative CLI, only loads csv files into a database for now.

## [21.12.0] - 2021-12-13
### Added
- First release on PyPI.

[Unreleased]: https://github.com/kipyin/pokemaster2/compare/v21.12.3...HEAD
[21.12.3]: https://github.com/kipyin/pokemaster2/compare/v21.12.2...v21.12.3
[21.12.2]: https://github.com/kipyin/pokemaster2/compare/v21.12.1...v21.12.2
[21.12.1]: https://github.com/kipyin/pokemaster2/compare/v21.12.0...v21.12.1

<!-- TOWNCRIER -->
