"""The pokedex database models."""
from typing import List

import peewee

database = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    """Base model for all tables."""

    class Meta:
        """Metadata for all tables."""

        database = database


class Region(BaseModel):
    """Major areas of the world: Kanto, Johto, etc."""

    identifier = peewee.CharField()

    class Meta:
        """Metadata for `Regions`."""

        table_name = "regions"


class Generation(BaseModel):
    """A Generation of the Pokémon franchise."""

    identifier = peewee.CharField()
    main_region = peewee.ForeignKeyField(
        column_name="main_region_id",
        field="id",
        model=Region,
        help_text="ID of the region this generation's main games take place in.",
    )

    class Meta:
        table_name = "generations"


class Ability(BaseModel):
    """An ability a Pokémon can have, such as Static or Pressure.

    IDs below 10000 match the internal ID in the games.
    IDs above 10000 are reserved for Conquest-only abilities.
    """

    generation = peewee.ForeignKeyField(
        column_name="generation_id",
        field="id",
        model=Generation,
        help_text="The ID of the generation this ability was introduced in.",
    )
    identifier = peewee.CharField()
    is_main_series = peewee.BooleanField(
        index=True, help_text="True iff the ability exists in the main series."
    )

    class Meta:
        table_name = "abilities"


class VersionGroups(BaseModel):
    """A group of versions.

    Containing either two paired versions (such as Red and Blue) or a single
    game (such as Yellow).
    """

    generation = peewee.ForeignKeyField(
        column_name="generation_id",
        field="id",
        model=Generation,
        help_text="The ID of the generation the games in this group belong to.",
    )
    identifier = peewee.CharField(unique=True)
    order = peewee.IntegerField(
        null=True,
        help_text="Order for sorting. Almost by date of release, except similar versions are grouped together.",
    )

    class Meta:
        table_name = "version_groups"


class AbilityChangelog(BaseModel):
    ability = peewee.ForeignKeyField(column_name="ability_id", field="id", model=Ability)
    changed_in_version_group = peewee.ForeignKeyField(
        column_name="changed_in_version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "ability_changelog"


class Languages(BaseModel):
    identifier = peewee.CharField()
    iso3166 = peewee.CharField()
    iso639 = peewee.CharField()
    official = peewee.BooleanField(index=True)
    order = peewee.IntegerField(null=True)

    class Meta:
        table_name = "languages"


class AbilityChangelogProse(BaseModel):
    ability_changelog = peewee.ForeignKeyField(
        column_name="ability_changelog_id", field="id", model=AbilityChangelog
    )
    effect = peewee.TextField()
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )

    class Meta:
        table_name = "ability_changelog_prose"
        indexes = ((("ability_changelog", "local_language"), True),)
        primary_key = peewee.CompositeKey("ability_changelog", "local_language")


class AbilityFlavorText(BaseModel):
    ability = peewee.ForeignKeyField(column_name="ability_id", field="id", model=Ability)
    flavor_text = peewee.TextField()
    language = peewee.ForeignKeyField(column_name="language_id", field="id", model=Languages)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "ability_flavor_text"
        indexes = ((("ability", "version_group", "language"), True),)
        primary_key = peewee.CompositeKey("ability", "language", "version_group")


class AbilityNames(BaseModel):
    ability = peewee.ForeignKeyField(column_name="ability_id", field="id", model=Ability)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "ability_names"
        indexes = ((("ability", "local_language"), True),)
        primary_key = peewee.CompositeKey("ability", "local_language")


class AbilityProse(BaseModel):
    ability = peewee.ForeignKeyField(column_name="ability_id", field="id", model=Ability)
    effect = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    short_effect = peewee.TextField(null=True)

    class Meta:
        table_name = "ability_prose"
        indexes = ((("ability", "local_language"), True),)
        primary_key = peewee.CompositeKey("ability", "local_language")


class MoveDamageClasses(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "move_damage_classes"


class Types(BaseModel):
    damage_class = peewee.ForeignKeyField(
        column_name="damage_class_id", field="id", model=MoveDamageClasses, null=True
    )
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    identifier = peewee.CharField()

    class Meta:
        table_name = "types"


class BerryFirmness(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "berry_firmness"


class ItemFlingEffects(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "item_fling_effects"


class ItemPockets(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "item_pockets"


class ItemCategories(BaseModel):
    identifier = peewee.CharField()
    pocket = peewee.ForeignKeyField(column_name="pocket_id", field="id", model=ItemPockets)

    class Meta:
        table_name = "item_categories"


class Items(BaseModel):
    category = peewee.ForeignKeyField(column_name="category_id", field="id", model=ItemCategories)
    cost = peewee.IntegerField()
    fling_effect = peewee.ForeignKeyField(
        column_name="fling_effect_id", field="id", model=ItemFlingEffects, null=True
    )
    fling_power = peewee.IntegerField(null=True)
    identifier = peewee.CharField()

    class Meta:
        table_name = "items"


class Berries(BaseModel):
    firmness = peewee.ForeignKeyField(column_name="firmness_id", field="id", model=BerryFirmness)
    growth_time = peewee.IntegerField()
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    max_harvest = peewee.IntegerField()
    natural_gift_power = peewee.IntegerField(null=True)
    natural_gift_type = peewee.ForeignKeyField(
        column_name="natural_gift_type_id", field="id", model=Types, null=True
    )
    size = peewee.IntegerField()
    smoothness = peewee.IntegerField()
    soil_dryness = peewee.IntegerField()

    class Meta:
        table_name = "berries"


class BerryFirmnessNames(BaseModel):
    berry_firmness = peewee.ForeignKeyField(
        column_name="berry_firmness_id", field="id", model=BerryFirmness
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "berry_firmness_names"
        indexes = ((("berry_firmness", "local_language"), True),)
        primary_key = peewee.CompositeKey("berry_firmness", "local_language")


class ContestTypes(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "contest_types"


class BerryFlavors(BaseModel):
    berry = peewee.ForeignKeyField(column_name="berry_id", field="id", model=Berries)
    contest_type = peewee.ForeignKeyField(
        column_name="contest_type_id", field="id", model=ContestTypes
    )
    flavor = peewee.IntegerField()

    class Meta:
        table_name = "berry_flavors"
        indexes = ((("berry", "contest_type"), True),)
        primary_key = peewee.CompositeKey("berry", "contest_type")


class Stats(BaseModel):
    damage_class = peewee.ForeignKeyField(
        column_name="damage_class_id", field="id", model=MoveDamageClasses, null=True
    )
    game_index = peewee.IntegerField(null=True)
    identifier = peewee.CharField()
    is_battle_only = peewee.BooleanField()

    class Meta:
        table_name = "stats"


class Characteristics(BaseModel):
    gene_mod_5 = peewee.IntegerField(index=True)
    stat = peewee.ForeignKeyField(column_name="stat_id", field="id", model=Stats)

    class Meta:
        table_name = "characteristics"


class CharacteristicText(BaseModel):
    characteristic = peewee.ForeignKeyField(
        column_name="characteristic_id", field="id", model=Characteristics
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    message = peewee.CharField(index=True)

    class Meta:
        table_name = "characteristic_text"
        indexes = ((("characteristic", "local_language"), True),)
        primary_key = peewee.CompositeKey("characteristic", "local_language")


class ConquestEpisodes(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "conquest_episodes"


class ConquestEpisodeNames(BaseModel):
    episode = peewee.ForeignKeyField(column_name="episode_id", field="id", model=ConquestEpisodes)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "conquest_episode_names"
        indexes = ((("episode", "local_language"), True),)
        primary_key = peewee.CompositeKey("episode", "local_language")


class ConquestWarriorArchetypes(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "conquest_warrior_archetypes"


class Genders(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "genders"


class ConquestWarriors(BaseModel):
    archetype = peewee.ForeignKeyField(
        column_name="archetype_id", field="id", model=ConquestWarriorArchetypes, null=True
    )
    gender = peewee.ForeignKeyField(column_name="gender_id", field="id", model=Genders)
    identifier = peewee.CharField()

    class Meta:
        table_name = "conquest_warriors"


class ConquestEpisodeWarriors(BaseModel):
    episode = peewee.ForeignKeyField(column_name="episode_id", field="id", model=ConquestEpisodes)
    warrior = peewee.ForeignKeyField(column_name="warrior_id", field="id", model=ConquestWarriors)

    class Meta:
        table_name = "conquest_episode_warriors"
        indexes = ((("episode", "warrior"), True),)
        primary_key = peewee.CompositeKey("episode", "warrior")


class ConquestKingdoms(BaseModel):
    identifier = peewee.CharField()
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types)

    class Meta:
        table_name = "conquest_kingdoms"


class ConquestKingdomNames(BaseModel):
    kingdom = peewee.ForeignKeyField(column_name="kingdom_id", field="id", model=ConquestKingdoms)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "conquest_kingdom_names"
        indexes = ((("kingdom", "local_language"), True),)
        primary_key = peewee.CompositeKey("kingdom", "local_language")


class GrowthRates(BaseModel):
    formula = peewee.TextField()
    identifier = peewee.CharField()

    class Meta:
        table_name = "growth_rates"


class PokemonHabitats(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "pokemon_habitats"


class PokemonShapes(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "pokemon_shapes"


class PokemonColors(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "pokemon_colors"


class EvolutionChains(BaseModel):
    baby_trigger_item = peewee.ForeignKeyField(
        column_name="baby_trigger_item_id", field="id", model=Items, null=True
    )

    class Meta:
        table_name = "evolution_chains"


class PokemonSpecies(BaseModel):
    base_happiness = peewee.IntegerField()
    capture_rate = peewee.IntegerField()
    color = peewee.ForeignKeyField(column_name="color_id", field="id", model=PokemonColors)
    conquest_order = peewee.IntegerField(index=True, null=True)
    evolution_chain = peewee.ForeignKeyField(
        column_name="evolution_chain_id", field="id", model=EvolutionChains, null=True
    )
    evolves_from_species = peewee.ForeignKeyField(
        column_name="evolves_from_species_id", field="id", model="self", null=True
    )
    forms_switchable = peewee.BooleanField()
    gender_rate = peewee.IntegerField()
    generation = peewee.ForeignKeyField(
        column_name="generation_id", field="id", model=Generation, null=True
    )
    growth_rate = peewee.ForeignKeyField(
        column_name="growth_rate_id", field="id", model=GrowthRates
    )
    habitat = peewee.ForeignKeyField(
        column_name="habitat_id", field="id", model=PokemonHabitats, null=True
    )
    has_gender_differences = peewee.BooleanField()
    hatch_counter = peewee.IntegerField()
    identifier = peewee.CharField()
    is_baby = peewee.BooleanField()
    is_legendary = peewee.BooleanField(
        null=False, help_text="True iff the Pokémon is a legendary Pokémon."
    )
    is_mythical = peewee.BooleanField(
        null=False, help_text="True iff the Pokémon is a mythical Pokémon."
    )
    order = peewee.IntegerField(index=True)
    shape = peewee.ForeignKeyField(column_name="shape_id", field="id", model=PokemonShapes)

    class Meta:
        table_name = "pokemon_species"


class ConquestWarriorSkills(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "conquest_warrior_skills"


class ConquestWarriorRanks(BaseModel):
    rank = peewee.IntegerField()
    skill = peewee.ForeignKeyField(column_name="skill_id", field="id", model=ConquestWarriorSkills)
    warrior = peewee.ForeignKeyField(column_name="warrior_id", field="id", model=ConquestWarriors)

    class Meta:
        table_name = "conquest_warrior_ranks"
        indexes = ((("warrior", "rank"), True),)


class ConquestMaxLinks(BaseModel):
    max_link = peewee.IntegerField()
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )
    warrior_rank = peewee.ForeignKeyField(
        column_name="warrior_rank_id", field="id", model=ConquestWarriorRanks
    )

    class Meta:
        table_name = "conquest_max_links"
        indexes = ((("warrior_rank", "pokemon_species"), True),)
        primary_key = peewee.CompositeKey("pokemon_species", "warrior_rank")


class ConquestMoveDisplacements(BaseModel):
    affects_target = peewee.BooleanField()
    identifier = peewee.CharField()

    class Meta:
        table_name = "conquest_move_displacements"


class ConquestMoveRanges(BaseModel):
    identifier = peewee.CharField()
    targets = peewee.IntegerField()

    class Meta:
        table_name = "conquest_move_ranges"


class ConquestMoveEffects(BaseModel):
    class Meta:
        table_name = "conquest_move_effects"


class SuperContestEffects(BaseModel):
    appeal = peewee.IntegerField()

    class Meta:
        table_name = "super_contest_effects"


class ContestEffects(BaseModel):
    appeal = peewee.IntegerField()
    jam = peewee.IntegerField()

    class Meta:
        table_name = "contest_effects"


class MoveEffects(BaseModel):
    class Meta:
        table_name = "move_effects"


class MoveTargets(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "move_targets"


class Moves(BaseModel):
    accuracy = peewee.IntegerField(null=True)
    contest_effect = peewee.ForeignKeyField(
        column_name="contest_effect_id", field="id", model=ContestEffects, null=True
    )
    contest_type = peewee.ForeignKeyField(
        column_name="contest_type_id", field="id", model=ContestTypes, null=True
    )
    damage_class = peewee.ForeignKeyField(
        column_name="damage_class_id", field="id", model=MoveDamageClasses
    )
    effect_chance = peewee.IntegerField(null=True)
    effect = peewee.ForeignKeyField(column_name="effect_id", field="id", model=MoveEffects)
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    identifier = peewee.CharField()
    power = peewee.IntegerField(null=True)
    pp = peewee.IntegerField(null=True)
    priority = peewee.IntegerField()
    super_contest_effect = peewee.ForeignKeyField(
        column_name="super_contest_effect_id", field="id", model=SuperContestEffects, null=True
    )
    target = peewee.ForeignKeyField(column_name="target_id", field="id", model=MoveTargets)
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types)

    class Meta:
        table_name = "moves"


class ConquestMoveData(BaseModel):
    accuracy = peewee.IntegerField(null=True)
    displacement = peewee.ForeignKeyField(
        column_name="displacement_id", field="id", model=ConquestMoveDisplacements, null=True
    )
    effect_chance = peewee.IntegerField(null=True)
    effect = peewee.ForeignKeyField(column_name="effect_id", field="id", model=ConquestMoveEffects)
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves, primary_key=True)
    power = peewee.IntegerField(null=True)
    range = peewee.ForeignKeyField(column_name="range_id", field="id", model=ConquestMoveRanges)

    class Meta:
        table_name = "conquest_move_data"


class ConquestMoveDisplacementProse(BaseModel):
    effect = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_displacement = peewee.ForeignKeyField(
        column_name="move_displacement_id", field="id", model=ConquestMoveDisplacements
    )
    name = peewee.CharField(null=True)
    short_effect = peewee.TextField(null=True)

    class Meta:
        table_name = "conquest_move_displacement_prose"
        indexes = ((("move_displacement", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_displacement")


class ConquestMoveEffectProse(BaseModel):
    conquest_move_effect = peewee.ForeignKeyField(
        column_name="conquest_move_effect_id", field="id", model=ConquestMoveEffects
    )
    effect = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    short_effect = peewee.TextField(null=True)

    class Meta:
        table_name = "conquest_move_effect_prose"
        indexes = ((("conquest_move_effect", "local_language"), True),)
        primary_key = peewee.CompositeKey("conquest_move_effect", "local_language")


class ConquestMoveRangeProse(BaseModel):
    conquest_move_range = peewee.ForeignKeyField(
        column_name="conquest_move_range_id", field="id", model=ConquestMoveRanges
    )
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(null=True)

    class Meta:
        table_name = "conquest_move_range_prose"
        indexes = ((("conquest_move_range", "local_language"), True),)
        primary_key = peewee.CompositeKey("conquest_move_range", "local_language")


class ConquestPokemonAbilities(BaseModel):
    ability = peewee.ForeignKeyField(column_name="ability_id", field="id", model=Ability)
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )
    slot = peewee.IntegerField()

    class Meta:
        table_name = "conquest_pokemon_abilities"
        indexes = ((("pokemon_species", "slot"), True),)
        primary_key = peewee.CompositeKey("pokemon_species", "slot")


class ConquestStats(BaseModel):
    identifier = peewee.CharField()
    is_base = peewee.BooleanField()

    class Meta:
        table_name = "conquest_stats"


class ConquestPokemonEvolution(BaseModel):
    evolved_species = peewee.ForeignKeyField(
        column_name="evolved_species_id", field="id", model=PokemonSpecies, primary_key=True
    )
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items, null=True)
    kingdom = peewee.ForeignKeyField(
        column_name="kingdom_id", field="id", model=ConquestKingdoms, null=True
    )
    minimum_link = peewee.IntegerField(null=True)
    minimum_stat = peewee.IntegerField(null=True)
    recruiting_ko_required = peewee.BooleanField()
    required_stat = peewee.ForeignKeyField(
        column_name="required_stat_id", field="id", model=ConquestStats, null=True
    )
    warrior_gender = peewee.ForeignKeyField(
        column_name="warrior_gender_id", field="id", model=Genders, null=True
    )

    class Meta:
        table_name = "conquest_pokemon_evolution"


class ConquestPokemonMoves(BaseModel):
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies, primary_key=True
    )

    class Meta:
        table_name = "conquest_pokemon_moves"


class ConquestPokemonStats(BaseModel):
    base_stat = peewee.IntegerField()
    conquest_stat = peewee.ForeignKeyField(
        column_name="conquest_stat_id", field="id", model=ConquestStats
    )
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )

    class Meta:
        table_name = "conquest_pokemon_stats"
        indexes = ((("pokemon_species", "conquest_stat"), True),)
        primary_key = peewee.CompositeKey("conquest_stat", "pokemon_species")


class ConquestStatNames(BaseModel):
    conquest_stat = peewee.ForeignKeyField(
        column_name="conquest_stat_id", field="id", model=ConquestStats
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "conquest_stat_names"
        indexes = ((("conquest_stat", "local_language"), True),)
        primary_key = peewee.CompositeKey("conquest_stat", "local_language")


class ConquestWarriorTransformation(BaseModel):
    collection_type = peewee.ForeignKeyField(
        column_name="collection_type_id", field="id", model=Types, null=True
    )
    completed_episode = peewee.ForeignKeyField(
        column_name="completed_episode_id", field="id", model=ConquestEpisodes, null=True
    )
    current_episode = peewee.ForeignKeyField(
        backref="conquest_episodes_current_episode_set",
        column_name="current_episode_id",
        field="id",
        model=ConquestEpisodes,
        null=True,
    )
    distant_warrior = peewee.ForeignKeyField(
        column_name="distant_warrior_id", field="id", model=ConquestWarriors, null=True
    )
    female_warlord_count = peewee.IntegerField(null=True)
    is_automatic = peewee.BooleanField()
    pokemon_count = peewee.IntegerField(null=True)
    required_link = peewee.IntegerField(null=True)
    transformed_warrior_rank = peewee.ForeignKeyField(
        column_name="transformed_warrior_rank_id",
        field="id",
        model=ConquestWarriorRanks,
        primary_key=True,
    )
    warrior_count = peewee.IntegerField(null=True)

    class Meta:
        table_name = "conquest_warrior_transformation"


class ConquestTransformationPokemon(BaseModel):
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )
    transformation = peewee.ForeignKeyField(
        column_name="transformation_id",
        field="transformed_warrior_rank",
        model=ConquestWarriorTransformation,
    )

    class Meta:
        table_name = "conquest_transformation_pokemon"
        indexes = ((("transformation", "pokemon_species"), True),)
        primary_key = peewee.CompositeKey("pokemon_species", "transformation")


class ConquestTransformationWarriors(BaseModel):
    present_warrior = peewee.ForeignKeyField(
        column_name="present_warrior_id", field="id", model=ConquestWarriors
    )
    transformation = peewee.ForeignKeyField(
        column_name="transformation_id",
        field="transformed_warrior_rank",
        model=ConquestWarriorTransformation,
    )

    class Meta:
        table_name = "conquest_transformation_warriors"
        indexes = ((("transformation", "present_warrior"), True),)
        primary_key = peewee.CompositeKey("present_warrior", "transformation")


class ConquestWarriorNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    warrior = peewee.ForeignKeyField(column_name="warrior_id", field="id", model=ConquestWarriors)

    class Meta:
        table_name = "conquest_warrior_names"
        indexes = ((("warrior", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "warrior")


class ConquestWarriorStats(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "conquest_warrior_stats"


class ConquestWarriorRankStatMap(BaseModel):
    base_stat = peewee.IntegerField()
    warrior_rank = peewee.ForeignKeyField(
        column_name="warrior_rank_id", field="id", model=ConquestWarriorRanks
    )
    warrior_stat = peewee.ForeignKeyField(
        column_name="warrior_stat_id", field="id", model=ConquestWarriorStats
    )

    class Meta:
        table_name = "conquest_warrior_rank_stat_map"
        indexes = ((("warrior_rank", "warrior_stat"), True),)
        primary_key = peewee.CompositeKey("warrior_rank", "warrior_stat")


class ConquestWarriorSkillNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    skill = peewee.ForeignKeyField(column_name="skill_id", field="id", model=ConquestWarriorSkills)

    class Meta:
        table_name = "conquest_warrior_skill_names"
        indexes = ((("skill", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "skill")


class ConquestWarriorSpecialties(BaseModel):
    slot = peewee.IntegerField()
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types)
    warrior = peewee.ForeignKeyField(column_name="warrior_id", field="id", model=ConquestWarriors)

    class Meta:
        table_name = "conquest_warrior_specialties"
        indexes = ((("warrior", "type", "slot"), True),)
        primary_key = peewee.CompositeKey("slot", "type", "warrior")


class ConquestWarriorStatNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    warrior_stat = peewee.ForeignKeyField(
        column_name="warrior_stat_id", field="id", model=ConquestWarriorStats
    )

    class Meta:
        table_name = "conquest_warrior_stat_names"
        indexes = ((("warrior_stat", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "warrior_stat")


class ContestCombos(BaseModel):
    first_move = peewee.ForeignKeyField(column_name="first_move_id", field="id", model=Moves)
    second_move = peewee.ForeignKeyField(
        backref="moves_second_move_set", column_name="second_move_id", field="id", model=Moves
    )

    class Meta:
        table_name = "contest_combos"
        indexes = ((("first_move", "second_move"), True),)
        primary_key = peewee.CompositeKey("first_move", "second_move")


class ContestEffectProse(BaseModel):
    contest_effect = peewee.ForeignKeyField(
        column_name="contest_effect_id", field="id", model=ContestEffects
    )
    effect = peewee.TextField(null=True)
    flavor_text = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )

    class Meta:
        table_name = "contest_effect_prose"
        indexes = ((("contest_effect", "local_language"), True),)
        primary_key = peewee.CompositeKey("contest_effect", "local_language")


class ContestTypeNames(BaseModel):
    color = peewee.TextField(null=True)
    contest_type = peewee.ForeignKeyField(
        column_name="contest_type_id", field="id", model=ContestTypes
    )
    flavor = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "contest_type_names"
        indexes = ((("contest_type", "local_language"), True),)
        primary_key = peewee.CompositeKey("contest_type", "local_language")


class EggGroups(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "egg_groups"


class EggGroupProse(BaseModel):
    egg_group = peewee.ForeignKeyField(column_name="egg_group_id", field="id", model=EggGroups)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "egg_group_prose"
        indexes = ((("egg_group", "local_language"), True),)
        primary_key = peewee.CompositeKey("egg_group", "local_language")


class EncounterConditions(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "encounter_conditions"


class EncounterConditionProse(BaseModel):
    encounter_condition = peewee.ForeignKeyField(
        column_name="encounter_condition_id", field="id", model=EncounterConditions
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "encounter_condition_prose"
        indexes = ((("encounter_condition", "local_language"), True),)
        primary_key = peewee.CompositeKey("encounter_condition", "local_language")


class EncounterConditionValues(BaseModel):
    encounter_condition = peewee.ForeignKeyField(
        column_name="encounter_condition_id", field="id", model=EncounterConditions
    )
    identifier = peewee.CharField()
    is_default = peewee.BooleanField()

    class Meta:
        table_name = "encounter_condition_values"


class Pokemon(BaseModel):
    base_experience = peewee.IntegerField()
    height = peewee.IntegerField()
    identifier = peewee.CharField()
    is_default = peewee.BooleanField(index=True)
    order = peewee.IntegerField(index=True)
    species = peewee.ForeignKeyField(
        column_name="species_id", field="id", model=PokemonSpecies, null=True
    )
    weight = peewee.IntegerField()

    class Meta:
        table_name = "pokemon"


class EncounterMethods(BaseModel):
    identifier = peewee.CharField(unique=True)
    order = peewee.IntegerField(unique=True)

    class Meta:
        table_name = "encounter_methods"


class EncounterSlots(BaseModel):
    encounter_method = peewee.ForeignKeyField(
        column_name="encounter_method_id", field="id", model=EncounterMethods
    )
    rarity = peewee.IntegerField(null=True)
    slot = peewee.IntegerField(null=True)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "encounter_slots"


class Locations(BaseModel):
    identifier = peewee.CharField(unique=True)
    region = peewee.ForeignKeyField(column_name="region_id", field="id", model=Region, null=True)

    class Meta:
        table_name = "locations"


class LocationAreas(BaseModel):
    game_index = peewee.IntegerField()
    identifier = peewee.CharField(null=True)
    location = peewee.ForeignKeyField(column_name="location_id", field="id", model=Locations)

    class Meta:
        table_name = "location_areas"
        indexes = ((("location", "identifier"), True),)


class Versions(BaseModel):
    identifier = peewee.CharField()
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "versions"


class Encounters(BaseModel):
    encounter_slot = peewee.ForeignKeyField(
        column_name="encounter_slot_id", field="id", model=EncounterSlots
    )
    location_area = peewee.ForeignKeyField(
        column_name="location_area_id", field="id", model=LocationAreas
    )
    max_level = peewee.IntegerField()
    min_level = peewee.IntegerField()
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    version = peewee.ForeignKeyField(column_name="version_id", field="id", model=Versions)

    class Meta:
        table_name = "encounters"


class EncounterConditionValueMap(BaseModel):
    encounter_condition_value = peewee.ForeignKeyField(
        column_name="encounter_condition_value_id", field="id", model=EncounterConditionValues
    )
    encounter = peewee.ForeignKeyField(column_name="encounter_id", field="id", model=Encounters)

    class Meta:
        table_name = "encounter_condition_value_map"
        indexes = ((("encounter", "encounter_condition_value"), True),)
        primary_key = peewee.CompositeKey("encounter", "encounter_condition_value")


class EncounterConditionValueProse(BaseModel):
    encounter_condition_value = peewee.ForeignKeyField(
        column_name="encounter_condition_value_id", field="id", model=EncounterConditionValues
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "encounter_condition_value_prose"
        indexes = ((("encounter_condition_value", "local_language"), True),)
        primary_key = peewee.CompositeKey("encounter_condition_value", "local_language")


class EncounterMethodProse(BaseModel):
    encounter_method = peewee.ForeignKeyField(
        column_name="encounter_method_id", field="id", model=EncounterMethods
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "encounter_method_prose"
        indexes = ((("encounter_method", "local_language"), True),)
        primary_key = peewee.CompositeKey("encounter_method", "local_language")


class EvolutionTriggers(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "evolution_triggers"


class EvolutionTriggerProse(BaseModel):
    evolution_trigger = peewee.ForeignKeyField(
        column_name="evolution_trigger_id", field="id", model=EvolutionTriggers
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "evolution_trigger_prose"
        indexes = ((("evolution_trigger", "local_language"), True),)
        primary_key = peewee.CompositeKey("evolution_trigger", "local_language")


class Experience(BaseModel):
    experience = peewee.IntegerField()
    growth_rate = peewee.ForeignKeyField(
        column_name="growth_rate_id", field="id", model=GrowthRates
    )
    level = peewee.IntegerField()

    class Meta:
        table_name = "experience"
        indexes = ((("growth_rate", "level"), True),)
        primary_key = peewee.CompositeKey("growth_rate", "level")


class GenerationNames(BaseModel):
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "generation_names"
        indexes = ((("generation", "local_language"), True),)
        primary_key = peewee.CompositeKey("generation", "local_language")


class GrowthRateProse(BaseModel):
    growth_rate = peewee.ForeignKeyField(
        column_name="growth_rate_id", field="id", model=GrowthRates
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "growth_rate_prose"
        indexes = ((("growth_rate", "local_language"), True),)
        primary_key = peewee.CompositeKey("growth_rate", "local_language")


class ItemCategoryProse(BaseModel):
    item_category = peewee.ForeignKeyField(
        column_name="item_category_id", field="id", model=ItemCategories
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "item_category_prose"
        indexes = ((("item_category", "local_language"), True),)
        primary_key = peewee.CompositeKey("item_category", "local_language")


class ItemFlags(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "item_flags"


class ItemFlagMap(BaseModel):
    item_flag = peewee.ForeignKeyField(column_name="item_flag_id", field="id", model=ItemFlags)
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)

    class Meta:
        table_name = "item_flag_map"
        indexes = ((("item", "item_flag"), True),)
        primary_key = peewee.CompositeKey("item", "item_flag")


class ItemFlagProse(BaseModel):
    description = peewee.TextField(null=True)
    item_flag = peewee.ForeignKeyField(column_name="item_flag_id", field="id", model=ItemFlags)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "item_flag_prose"
        indexes = ((("item_flag", "local_language"), True),)
        primary_key = peewee.CompositeKey("item_flag", "local_language")


class ItemFlavorSummaries(BaseModel):
    flavor_summary = peewee.TextField(null=True)
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )

    class Meta:
        table_name = "item_flavor_summaries"
        indexes = ((("item", "local_language"), True),)
        primary_key = peewee.CompositeKey("item", "local_language")


class ItemFlavorText(BaseModel):
    flavor_text = peewee.TextField()
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    language = peewee.ForeignKeyField(column_name="language_id", field="id", model=Languages)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "item_flavor_text"
        indexes = ((("item", "version_group", "language"), True),)
        primary_key = peewee.CompositeKey("item", "language", "version_group")


class ItemFlingEffectProse(BaseModel):
    effect = peewee.TextField()
    item_fling_effect = peewee.ForeignKeyField(
        column_name="item_fling_effect_id", field="id", model=ItemFlingEffects
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )

    class Meta:
        table_name = "item_fling_effect_prose"
        indexes = ((("item_fling_effect", "local_language"), True),)
        primary_key = peewee.CompositeKey("item_fling_effect", "local_language")


class ItemGameIndices(BaseModel):
    game_index = peewee.IntegerField()
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)

    class Meta:
        table_name = "item_game_indices"
        indexes = ((("item", "generation"), True),)
        primary_key = peewee.CompositeKey("generation", "item")


class ItemNames(BaseModel):
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "item_names"
        indexes = ((("item", "local_language"), True),)
        primary_key = peewee.CompositeKey("item", "local_language")


class ItemPocketNames(BaseModel):
    item_pocket = peewee.ForeignKeyField(
        column_name="item_pocket_id", field="id", model=ItemPockets
    )
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "item_pocket_names"
        indexes = ((("item_pocket", "local_language"), True),)
        primary_key = peewee.CompositeKey("item_pocket", "local_language")


class ItemProse(BaseModel):
    effect = peewee.TextField(null=True)
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    short_effect = peewee.TextField(null=True)

    class Meta:
        table_name = "item_prose"
        indexes = ((("item", "local_language"), True),)
        primary_key = peewee.CompositeKey("item", "local_language")


class LanguageNames(BaseModel):
    language = peewee.ForeignKeyField(column_name="language_id", field="id", model=Languages)
    local_language = peewee.ForeignKeyField(
        backref="languages_local_language_set",
        column_name="local_language_id",
        field="id",
        model=Languages,
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "language_names"
        indexes = ((("language", "local_language"), True),)
        primary_key = peewee.CompositeKey("language", "local_language")


class LocationAreaEncounterRates(BaseModel):
    encounter_method = peewee.ForeignKeyField(
        column_name="encounter_method_id", field="id", model=EncounterMethods
    )
    location_area = peewee.ForeignKeyField(
        column_name="location_area_id", field="id", model=LocationAreas
    )
    rate = peewee.IntegerField(null=True)
    version = peewee.ForeignKeyField(column_name="version_id", field="id", model=Versions)

    class Meta:
        table_name = "location_area_encounter_rates"
        indexes = ((("location_area", "encounter_method", "version"), True),)
        primary_key = peewee.CompositeKey("encounter_method", "location_area", "version")


class LocationAreaProse(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    location_area = peewee.ForeignKeyField(
        column_name="location_area_id", field="id", model=LocationAreas
    )
    name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "location_area_prose"
        indexes = ((("location_area", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "location_area")


class LocationGameIndices(BaseModel):
    game_index = peewee.IntegerField()
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    location = peewee.ForeignKeyField(column_name="location_id", field="id", model=Locations)

    class Meta:
        table_name = "location_game_indices"
        indexes = ((("location", "generation", "game_index"), True),)
        primary_key = peewee.CompositeKey("game_index", "generation", "location")


class LocationNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    location = peewee.ForeignKeyField(column_name="location_id", field="id", model=Locations)
    name = peewee.CharField(index=True)
    subtitle = peewee.CharField(null=True)

    class Meta:
        table_name = "location_names"
        indexes = ((("location", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "location")


class Machines(BaseModel):
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    machine_number = peewee.IntegerField()
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "machines"
        indexes = ((("machine_number", "version_group"), True),)
        primary_key = peewee.CompositeKey("machine_number", "version_group")


class MoveBattleStyles(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "move_battle_styles"


class MoveBattleStyleProse(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_battle_style = peewee.ForeignKeyField(
        column_name="move_battle_style_id", field="id", model=MoveBattleStyles
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "move_battle_style_prose"
        indexes = ((("move_battle_style", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_battle_style")


class MoveChangelog(BaseModel):
    accuracy = peewee.IntegerField(null=True)
    changed_in_version_group = peewee.ForeignKeyField(
        column_name="changed_in_version_group_id", field="id", model=VersionGroups
    )
    effect_chance = peewee.IntegerField(null=True)
    effect = peewee.ForeignKeyField(
        column_name="effect_id", field="id", model=MoveEffects, null=True
    )
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    power = peewee.IntegerField(null=True)
    pp = peewee.IntegerField(null=True)
    priority = peewee.IntegerField(null=True)
    target = peewee.ForeignKeyField(
        column_name="target_id", field="id", model=MoveTargets, null=True
    )
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types, null=True)

    class Meta:
        table_name = "move_changelog"
        indexes = ((("move", "changed_in_version_group"), True),)
        primary_key = peewee.CompositeKey("changed_in_version_group", "move")


class MoveDamageClassProse(BaseModel):
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_damage_class = peewee.ForeignKeyField(
        column_name="move_damage_class_id", field="id", model=MoveDamageClasses
    )
    name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "move_damage_class_prose"
        indexes = ((("move_damage_class", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_damage_class")


class MoveEffectChangelog(BaseModel):
    changed_in_version_group = peewee.ForeignKeyField(
        column_name="changed_in_version_group_id", field="id", model=VersionGroups
    )
    effect = peewee.ForeignKeyField(column_name="effect_id", field="id", model=MoveEffects)

    class Meta:
        table_name = "move_effect_changelog"
        indexes = ((("effect", "changed_in_version_group"), True),)


class MoveEffectChangelogProse(BaseModel):
    effect = peewee.TextField()
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_effect_changelog = peewee.ForeignKeyField(
        column_name="move_effect_changelog_id", field="id", model=MoveEffectChangelog
    )

    class Meta:
        table_name = "move_effect_changelog_prose"
        indexes = ((("move_effect_changelog", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_effect_changelog")


class MoveEffectProse(BaseModel):
    effect = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_effect = peewee.ForeignKeyField(
        column_name="move_effect_id", field="id", model=MoveEffects
    )
    short_effect = peewee.TextField(null=True)

    class Meta:
        table_name = "move_effect_prose"
        indexes = ((("move_effect", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_effect")


class MoveFlags(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "move_flags"


class MoveFlagMap(BaseModel):
    move_flag = peewee.ForeignKeyField(column_name="move_flag_id", field="id", model=MoveFlags)
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)

    class Meta:
        table_name = "move_flag_map"
        indexes = ((("move", "move_flag"), True),)
        primary_key = peewee.CompositeKey("move", "move_flag")


class MoveFlagProse(BaseModel):
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_flag = peewee.ForeignKeyField(column_name="move_flag_id", field="id", model=MoveFlags)
    name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "move_flag_prose"
        indexes = ((("move_flag", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_flag")


class MoveFlavorSummaries(BaseModel):
    flavor_summary = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)

    class Meta:
        table_name = "move_flavor_summaries"
        indexes = ((("move", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move")


class MoveFlavorText(BaseModel):
    flavor_text = peewee.TextField()
    language = peewee.ForeignKeyField(column_name="language_id", field="id", model=Languages)
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "move_flavor_text"
        indexes = ((("move", "version_group", "language"), True),)
        primary_key = peewee.CompositeKey("language", "move", "version_group")


class MoveMetaAilments(BaseModel):
    identifier = peewee.CharField(unique=True)

    class Meta:
        table_name = "move_meta_ailments"


class MoveMetaCategories(BaseModel):
    identifier = peewee.CharField(unique=True)

    class Meta:
        table_name = "move_meta_categories"


class MoveMeta(BaseModel):
    ailment_chance = peewee.IntegerField(index=True)
    crit_rate = peewee.IntegerField(index=True)
    drain = peewee.IntegerField(index=True)
    flinch_chance = peewee.IntegerField(index=True)
    healing = peewee.IntegerField(index=True)
    max_hits = peewee.IntegerField(index=True, null=True)
    max_turns = peewee.IntegerField(index=True, null=True)
    meta_ailment = peewee.ForeignKeyField(
        column_name="meta_ailment_id", field="id", model=MoveMetaAilments
    )
    meta_category = peewee.ForeignKeyField(
        column_name="meta_category_id", field="id", model=MoveMetaCategories
    )
    min_hits = peewee.IntegerField(index=True, null=True)
    min_turns = peewee.IntegerField(index=True, null=True)
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves, primary_key=True)
    stat_chance = peewee.IntegerField(index=True)

    class Meta:
        table_name = "move_meta"


class MoveMetaAilmentNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_meta_ailment = peewee.ForeignKeyField(
        column_name="move_meta_ailment_id", field="id", model=MoveMetaAilments
    )
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "move_meta_ailment_names"
        indexes = ((("move_meta_ailment", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_meta_ailment")


class MoveMetaCategoryProse(BaseModel):
    description = peewee.TextField()
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_meta_category = peewee.ForeignKeyField(
        column_name="move_meta_category_id", field="id", model=MoveMetaCategories
    )

    class Meta:
        table_name = "move_meta_category_prose"
        indexes = ((("move_meta_category", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_meta_category")


class MoveMetaStatChanges(BaseModel):
    change = peewee.IntegerField(index=True)
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    stat = peewee.ForeignKeyField(column_name="stat_id", field="id", model=Stats)

    class Meta:
        table_name = "move_meta_stat_changes"
        indexes = ((("move", "stat"), True),)
        primary_key = peewee.CompositeKey("move", "stat")


class MoveNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    name = peewee.CharField(index=True)

    class Meta:
        table_name = "move_names"
        indexes = ((("move", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move")


class MoveTargetProse(BaseModel):
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    move_target = peewee.ForeignKeyField(
        column_name="move_target_id", field="id", model=MoveTargets
    )
    name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "move_target_prose"
        indexes = ((("move_target", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "move_target")


class Natures(BaseModel):
    decreased_stat = peewee.ForeignKeyField(
        column_name="decreased_stat_id", field="id", model=Stats
    )
    game_index = peewee.IntegerField(unique=True)
    hates_flavor = peewee.ForeignKeyField(
        column_name="hates_flavor_id", field="id", model=ContestTypes
    )
    identifier = peewee.CharField()
    increased_stat = peewee.ForeignKeyField(
        backref="stats_increased_stat_set",
        column_name="increased_stat_id",
        field="id",
        model=Stats,
    )
    likes_flavor = peewee.ForeignKeyField(
        backref="contest_types_likes_flavor_set",
        column_name="likes_flavor_id",
        field="id",
        model=ContestTypes,
    )

    class Meta:
        table_name = "natures"


class NatureBattleStylePreferences(BaseModel):
    high_hp_preference = peewee.IntegerField()
    low_hp_preference = peewee.IntegerField()
    move_battle_style = peewee.ForeignKeyField(
        column_name="move_battle_style_id", field="id", model=MoveBattleStyles
    )
    nature = peewee.ForeignKeyField(column_name="nature_id", field="id", model=Natures)

    class Meta:
        table_name = "nature_battle_style_preferences"
        indexes = ((("nature", "move_battle_style"), True),)
        primary_key = peewee.CompositeKey("move_battle_style", "nature")


class NatureNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    nature = peewee.ForeignKeyField(column_name="nature_id", field="id", model=Natures)

    class Meta:
        table_name = "nature_names"
        indexes = ((("nature", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "nature")


class PokeathlonStats(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "pokeathlon_stats"


class NaturePokeathlonStats(BaseModel):
    max_change = peewee.IntegerField()
    nature = peewee.ForeignKeyField(column_name="nature_id", field="id", model=Natures)
    pokeathlon_stat = peewee.ForeignKeyField(
        column_name="pokeathlon_stat_id", field="id", model=PokeathlonStats
    )

    class Meta:
        table_name = "nature_pokeathlon_stats"
        indexes = ((("nature", "pokeathlon_stat"), True),)
        primary_key = peewee.CompositeKey("nature", "pokeathlon_stat")


class PalParkAreas(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "pal_park_areas"


class PalPark(BaseModel):
    area = peewee.ForeignKeyField(column_name="area_id", field="id", model=PalParkAreas)
    base_score = peewee.IntegerField()
    rate = peewee.IntegerField()
    species = peewee.ForeignKeyField(
        column_name="species_id", field="id", model=PokemonSpecies, primary_key=True
    )

    class Meta:
        table_name = "pal_park"


class PalParkAreaNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    pal_park_area = peewee.ForeignKeyField(
        column_name="pal_park_area_id", field="id", model=PalParkAreas
    )

    class Meta:
        table_name = "pal_park_area_names"
        indexes = ((("pal_park_area", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pal_park_area")


class PokeathlonStatNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    pokeathlon_stat = peewee.ForeignKeyField(
        column_name="pokeathlon_stat_id", field="id", model=PokeathlonStats
    )

    class Meta:
        table_name = "pokeathlon_stat_names"
        indexes = ((("pokeathlon_stat", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokeathlon_stat")


class Pokedexes(BaseModel):
    identifier = peewee.CharField()
    is_main_series = peewee.BooleanField()
    region = peewee.ForeignKeyField(column_name="region_id", field="id", model=Region, null=True)

    class Meta:
        table_name = "pokedexes"


class PokedexProse(BaseModel):
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True, null=True)
    pokedex = peewee.ForeignKeyField(column_name="pokedex_id", field="id", model=Pokedexes)

    class Meta:
        table_name = "pokedex_prose"
        indexes = ((("pokedex", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokedex")


class PokedexVersionGroups(BaseModel):
    pokedex = peewee.ForeignKeyField(column_name="pokedex_id", field="id", model=Pokedexes)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "pokedex_version_groups"
        indexes = ((("pokedex", "version_group"), True),)
        primary_key = peewee.CompositeKey("pokedex", "version_group")


class PokemonAbilities(BaseModel):
    ability = peewee.ForeignKeyField(column_name="ability_id", field="id", model=Ability)
    is_hidden = peewee.BooleanField(index=True)
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    slot = peewee.IntegerField()

    class Meta:
        table_name = "pokemon_abilities"
        indexes = ((("pokemon", "slot"), True),)
        primary_key = peewee.CompositeKey("pokemon", "slot")


class PokemonColorNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    pokemon_color = peewee.ForeignKeyField(
        column_name="pokemon_color_id", field="id", model=PokemonColors
    )

    class Meta:
        table_name = "pokemon_color_names"
        indexes = ((("pokemon_color", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_color")


class PokemonDexNumbers(BaseModel):
    pokedex = peewee.ForeignKeyField(column_name="pokedex_id", field="id", model=Pokedexes)
    pokedex_number = peewee.IntegerField()
    species = peewee.ForeignKeyField(column_name="species_id", field="id", model=PokemonSpecies)

    class Meta:
        table_name = "pokemon_dex_numbers"
        indexes = ((("species", "pokedex"), True),)
        primary_key = peewee.CompositeKey("pokedex", "species")


class PokemonEggGroups(BaseModel):
    egg_group = peewee.ForeignKeyField(column_name="egg_group_id", field="id", model=EggGroups)
    species = peewee.ForeignKeyField(column_name="species_id", field="id", model=PokemonSpecies)

    class Meta:
        table_name = "pokemon_egg_groups"
        indexes = ((("species", "egg_group"), True),)
        primary_key = peewee.CompositeKey("egg_group", "species")


class PokemonEvolution(BaseModel):
    evolution_trigger = peewee.ForeignKeyField(
        column_name="evolution_trigger_id", field="id", model=EvolutionTriggers
    )
    evolved_species = peewee.ForeignKeyField(
        column_name="evolved_species_id", field="id", model=PokemonSpecies
    )
    gender = peewee.ForeignKeyField(column_name="gender_id", field="id", model=Genders, null=True)
    held_item = peewee.ForeignKeyField(
        column_name="held_item_id", field="id", model=Items, null=True
    )
    known_move = peewee.ForeignKeyField(
        column_name="known_move_id", field="id", model=Moves, null=True
    )
    known_move_type = peewee.ForeignKeyField(
        column_name="known_move_type_id", field="id", model=Types, null=True
    )
    location = peewee.ForeignKeyField(
        column_name="location_id", field="id", model=Locations, null=True
    )
    minimum_affection = peewee.IntegerField(null=True)
    minimum_beauty = peewee.IntegerField(null=True)
    minimum_happiness = peewee.IntegerField(null=True)
    minimum_level = peewee.IntegerField(null=True)
    needs_overworld_rain = peewee.BooleanField()
    party_species = peewee.ForeignKeyField(
        backref="pokemon_species_party_species_set",
        column_name="party_species_id",
        field="id",
        model=PokemonSpecies,
        null=True,
    )
    party_type = peewee.ForeignKeyField(
        backref="types_party_type_set",
        column_name="party_type_id",
        field="id",
        model=Types,
        null=True,
    )
    relative_physical_stats = peewee.IntegerField(null=True)
    time_of_day = peewee.CharField(null=True)
    trade_species = peewee.ForeignKeyField(
        backref="pokemon_species_trade_species_set",
        column_name="trade_species_id",
        field="id",
        model=PokemonSpecies,
        null=True,
    )
    trigger_item = peewee.ForeignKeyField(
        backref="items_trigger_item_set",
        column_name="trigger_item_id",
        field="id",
        model=Items,
        null=True,
    )
    turn_upside_down = peewee.BooleanField()

    class Meta:
        table_name = "pokemon_evolution"


class PokemonForms(BaseModel):
    form_identifier = peewee.CharField(null=True)
    form_order = peewee.IntegerField()
    identifier = peewee.CharField()
    introduced_in_version_group = peewee.ForeignKeyField(
        column_name="introduced_in_version_group_id", field="id", model=VersionGroups, null=True
    )
    is_battle_only = peewee.BooleanField()
    is_default = peewee.BooleanField()
    is_mega = peewee.BooleanField()
    order = peewee.IntegerField()
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)

    class Meta:
        table_name = "pokemon_forms"


class PokemonFormGenerations(BaseModel):
    game_index = peewee.IntegerField()
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    pokemon_form = peewee.ForeignKeyField(
        column_name="pokemon_form_id", field="id", model=PokemonForms
    )

    class Meta:
        table_name = "pokemon_form_generations"
        indexes = ((("pokemon_form", "generation"), True),)
        primary_key = peewee.CompositeKey("generation", "pokemon_form")


class PokemonFormNames(BaseModel):
    form_name = peewee.CharField(index=True, null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    pokemon_form = peewee.ForeignKeyField(
        column_name="pokemon_form_id", field="id", model=PokemonForms
    )
    pokemon_name = peewee.CharField(index=True, null=True)

    class Meta:
        table_name = "pokemon_form_names"
        indexes = ((("pokemon_form", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_form")


class PokemonFormPokeathlonStats(BaseModel):
    base_stat = peewee.IntegerField()
    maximum_stat = peewee.IntegerField()
    minimum_stat = peewee.IntegerField()
    pokeathlon_stat = peewee.ForeignKeyField(
        column_name="pokeathlon_stat_id", field="id", model=PokeathlonStats
    )
    pokemon_form = peewee.ForeignKeyField(
        column_name="pokemon_form_id", field="id", model=PokemonForms
    )

    class Meta:
        table_name = "pokemon_form_pokeathlon_stats"
        indexes = ((("pokemon_form", "pokeathlon_stat"), True),)
        primary_key = peewee.CompositeKey("pokeathlon_stat", "pokemon_form")


class PokemonGameIndices(BaseModel):
    game_index = peewee.IntegerField()
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    version = peewee.ForeignKeyField(column_name="version_id", field="id", model=Versions)

    class Meta:
        table_name = "pokemon_game_indices"
        indexes = ((("pokemon", "version"), True),)
        primary_key = peewee.CompositeKey("pokemon", "version")


class PokemonHabitatNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    pokemon_habitat = peewee.ForeignKeyField(
        column_name="pokemon_habitat_id", field="id", model=PokemonHabitats
    )

    class Meta:
        table_name = "pokemon_habitat_names"
        indexes = ((("pokemon_habitat", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_habitat")


class PokemonItems(BaseModel):
    item = peewee.ForeignKeyField(column_name="item_id", field="id", model=Items)
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    rarity = peewee.IntegerField()
    version = peewee.ForeignKeyField(column_name="version_id", field="id", model=Versions)

    class Meta:
        table_name = "pokemon_items"
        indexes = ((("pokemon", "version", "item"), True),)
        primary_key = peewee.CompositeKey("item", "pokemon", "version")


class PokemonMoveMethods(BaseModel):
    identifier = peewee.CharField()

    class Meta:
        table_name = "pokemon_move_methods"


class PokemonMoveMethodProse(BaseModel):
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True, null=True)
    pokemon_move_method = peewee.ForeignKeyField(
        column_name="pokemon_move_method_id", field="id", model=PokemonMoveMethods
    )

    class Meta:
        table_name = "pokemon_move_method_prose"
        indexes = ((("pokemon_move_method", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_move_method")


class PokemonMoves(BaseModel):
    level = peewee.IntegerField(index=True)
    move = peewee.ForeignKeyField(column_name="move_id", field="id", model=Moves)
    order = peewee.IntegerField(null=True)
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    pokemon_move_method = peewee.ForeignKeyField(
        column_name="pokemon_move_method_id", field="id", model=PokemonMoveMethods
    )
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "pokemon_moves"
        indexes = ((("pokemon", "version_group", "move", "pokemon_move_method", "level"), True),)
        primary_key = peewee.CompositeKey(
            "level", "move", "pokemon", "pokemon_move_method", "version_group"
        )


class PokemonShapeProse(BaseModel):
    awesome_name = peewee.CharField(null=True)
    description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True, null=True)
    pokemon_shape = peewee.ForeignKeyField(
        column_name="pokemon_shape_id", field="id", model=PokemonShapes
    )

    class Meta:
        table_name = "pokemon_shape_prose"
        indexes = ((("pokemon_shape", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_shape")


class PokemonSpeciesFlavorSummaries(BaseModel):
    flavor_summary = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )

    class Meta:
        table_name = "pokemon_species_flavor_summaries"
        indexes = ((("pokemon_species", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_species")


class PokemonSpeciesFlavorText(BaseModel):
    flavor_text = peewee.TextField()
    language = peewee.ForeignKeyField(column_name="language_id", field="id", model=Languages)
    species = peewee.ForeignKeyField(column_name="species_id", field="id", model=PokemonSpecies)
    version = peewee.ForeignKeyField(column_name="version_id", field="id", model=Versions)

    class Meta:
        table_name = "pokemon_species_flavor_text"
        indexes = ((("species", "version", "language"), True),)
        primary_key = peewee.CompositeKey("language", "species", "version")


class PokemonSpeciesNames(BaseModel):
    genus = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True, null=True)
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )

    class Meta:
        table_name = "pokemon_species_names"
        indexes = ((("pokemon_species", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_species")


class PokemonSpeciesProse(BaseModel):
    form_description = peewee.TextField(null=True)
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    pokemon_species = peewee.ForeignKeyField(
        column_name="pokemon_species_id", field="id", model=PokemonSpecies
    )

    class Meta:
        table_name = "pokemon_species_prose"
        indexes = ((("pokemon_species", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "pokemon_species")


class PokemonStats(BaseModel):
    base_stat = peewee.IntegerField()
    effort = peewee.IntegerField()
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    stat = peewee.ForeignKeyField(column_name="stat_id", field="id", model=Stats)

    class Meta:
        table_name = "pokemon_stats"
        indexes = ((("pokemon", "stat"), True),)
        primary_key = peewee.CompositeKey("pokemon", "stat")


class PokemonTypes(BaseModel):
    pokemon = peewee.ForeignKeyField(column_name="pokemon_id", field="id", model=Pokemon)
    slot = peewee.IntegerField()
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types)

    class Meta:
        table_name = "pokemon_types"
        indexes = ((("pokemon", "slot"), True),)
        primary_key = peewee.CompositeKey("pokemon", "slot")


class RegionNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    region = peewee.ForeignKeyField(column_name="region_id", field="id", model=Region)

    class Meta:
        table_name = "region_names"
        indexes = ((("region", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "region")


class StatNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    stat = peewee.ForeignKeyField(column_name="stat_id", field="id", model=Stats)

    class Meta:
        table_name = "stat_names"
        indexes = ((("stat", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "stat")


class SuperContestCombos(BaseModel):
    first_move = peewee.ForeignKeyField(column_name="first_move_id", field="id", model=Moves)
    second_move = peewee.ForeignKeyField(
        backref="moves_second_move_set", column_name="second_move_id", field="id", model=Moves
    )

    class Meta:
        table_name = "super_contest_combos"
        indexes = ((("first_move", "second_move"), True),)
        primary_key = peewee.CompositeKey("first_move", "second_move")


class SuperContestEffectProse(BaseModel):
    flavor_text = peewee.TextField()
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    super_contest_effect = peewee.ForeignKeyField(
        column_name="super_contest_effect_id", field="id", model=SuperContestEffects
    )

    class Meta:
        table_name = "super_contest_effect_prose"
        indexes = ((("super_contest_effect", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "super_contest_effect")


class TypeEfficacy(BaseModel):
    damage_factor = peewee.IntegerField()
    damage_type = peewee.ForeignKeyField(column_name="damage_type_id", field="id", model=Types)
    target_type = peewee.ForeignKeyField(
        backref="types_target_type_set", column_name="target_type_id", field="id", model=Types
    )

    class Meta:
        table_name = "type_efficacy"
        indexes = ((("damage_type", "target_type"), True),)
        primary_key = peewee.CompositeKey("damage_type", "target_type")


class TypeGameIndices(BaseModel):
    game_index = peewee.IntegerField()
    generation = peewee.ForeignKeyField(column_name="generation_id", field="id", model=Generation)
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types)

    class Meta:
        table_name = "type_game_indices"
        indexes = ((("type", "generation"), True),)
        primary_key = peewee.CompositeKey("generation", "type")


class TypeNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    type = peewee.ForeignKeyField(column_name="type_id", field="id", model=Types)

    class Meta:
        table_name = "type_names"
        indexes = ((("type", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "type")


class VersionGroupPokemonMoveMethods(BaseModel):
    pokemon_move_method = peewee.ForeignKeyField(
        column_name="pokemon_move_method_id", field="id", model=PokemonMoveMethods
    )
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "version_group_pokemon_move_methods"
        indexes = ((("version_group", "pokemon_move_method"), True),)
        primary_key = peewee.CompositeKey("pokemon_move_method", "version_group")


class VersionGroupRegions(BaseModel):
    region = peewee.ForeignKeyField(column_name="region_id", field="id", model=Region)
    version_group = peewee.ForeignKeyField(
        column_name="version_group_id", field="id", model=VersionGroups
    )

    class Meta:
        table_name = "version_group_regions"
        indexes = ((("version_group", "region"), True),)
        primary_key = peewee.CompositeKey("region", "version_group")


class VersionNames(BaseModel):
    local_language = peewee.ForeignKeyField(
        column_name="local_language_id", field="id", model=Languages
    )
    name = peewee.CharField(index=True)
    version = peewee.ForeignKeyField(column_name="version_id", field="id", model=Versions)

    class Meta:
        table_name = "version_names"
        indexes = ((("version", "local_language"), True),)
        primary_key = peewee.CompositeKey("local_language", "version")


def get_pokemon(identifier: str) -> List[Pokemon]:
    """Find a single `Pokemon` instance."""
    pokemon_set = (
        Pokemon.select(Pokemon, PokemonSpecies)
        .join(PokemonSpecies)
        .where(Pokemon.identifier == identifier)
    )

    return pokemon_set


MODELS = [
    Ability,
    AbilityChangelog,
    AbilityChangelogProse,
    AbilityFlavorText,
    AbilityNames,
    AbilityProse,
    Berries,
    BerryFirmness,
    BerryFirmnessNames,
    BerryFlavors,
    CharacteristicText,
    Characteristics,
    ConquestEpisodeNames,
    ConquestEpisodeWarriors,
    ConquestEpisodes,
    ConquestKingdomNames,
    ConquestKingdoms,
    ConquestMaxLinks,
    ConquestMoveData,
    ConquestMoveDisplacementProse,
    ConquestMoveDisplacements,
    ConquestMoveEffectProse,
    ConquestMoveEffects,
    ConquestMoveRangeProse,
    ConquestMoveRanges,
    ConquestPokemonAbilities,
    ConquestPokemonEvolution,
    ConquestPokemonMoves,
    ConquestPokemonStats,
    ConquestStatNames,
    ConquestStats,
    ConquestTransformationPokemon,
    ConquestTransformationWarriors,
    ConquestWarriorArchetypes,
    ConquestWarriorNames,
    ConquestWarriorRankStatMap,
    ConquestWarriorRanks,
    ConquestWarriorSkillNames,
    ConquestWarriorSkills,
    ConquestWarriorSpecialties,
    ConquestWarriorStatNames,
    ConquestWarriorStats,
    ConquestWarriorTransformation,
    ConquestWarriors,
    ContestCombos,
    ContestEffectProse,
    ContestEffects,
    ContestTypeNames,
    ContestTypes,
    EggGroupProse,
    EggGroups,
    EncounterConditionProse,
    EncounterConditionValueMap,
    EncounterConditionValueProse,
    EncounterConditionValues,
    EncounterConditions,
    EncounterMethodProse,
    EncounterMethods,
    EncounterSlots,
    Encounters,
    EvolutionChains,
    EvolutionTriggerProse,
    EvolutionTriggers,
    Experience,
    Genders,
    GenerationNames,
    Generation,
    GrowthRateProse,
    GrowthRates,
    ItemCategories,
    ItemCategoryProse,
    ItemFlagMap,
    ItemFlagProse,
    ItemFlags,
    ItemFlavorSummaries,
    ItemFlavorText,
    ItemFlingEffectProse,
    ItemFlingEffects,
    ItemGameIndices,
    ItemNames,
    ItemPocketNames,
    ItemPockets,
    ItemProse,
    Items,
    LanguageNames,
    Languages,
    LocationAreaEncounterRates,
    LocationAreaProse,
    LocationAreas,
    LocationGameIndices,
    LocationNames,
    Locations,
    Machines,
    MoveBattleStyleProse,
    MoveBattleStyles,
    MoveChangelog,
    MoveDamageClassProse,
    MoveDamageClasses,
    MoveEffectChangelog,
    MoveEffectChangelogProse,
    MoveEffectProse,
    MoveEffects,
    MoveFlagMap,
    MoveFlagProse,
    MoveFlags,
    MoveFlavorSummaries,
    MoveFlavorText,
    MoveMeta,
    MoveMetaAilmentNames,
    MoveMetaAilments,
    MoveMetaCategories,
    MoveMetaCategoryProse,
    MoveMetaStatChanges,
    MoveNames,
    MoveTargetProse,
    MoveTargets,
    Moves,
    NatureBattleStylePreferences,
    NatureNames,
    NaturePokeathlonStats,
    Natures,
    PalPark,
    PalParkAreaNames,
    PalParkAreas,
    PokeathlonStatNames,
    PokeathlonStats,
    PokedexProse,
    PokedexVersionGroups,
    Pokedexes,
    Pokemon,
    PokemonAbilities,
    PokemonColorNames,
    PokemonColors,
    PokemonDexNumbers,
    PokemonEggGroups,
    PokemonEvolution,
    PokemonFormGenerations,
    PokemonFormNames,
    PokemonFormPokeathlonStats,
    PokemonForms,
    PokemonGameIndices,
    PokemonHabitatNames,
    PokemonHabitats,
    PokemonItems,
    PokemonMoveMethodProse,
    PokemonMoveMethods,
    PokemonMoves,
    PokemonShapeProse,
    PokemonShapes,
    PokemonSpecies,
    PokemonSpeciesFlavorSummaries,
    PokemonSpeciesFlavorText,
    PokemonSpeciesNames,
    PokemonSpeciesProse,
    PokemonStats,
    PokemonTypes,
    RegionNames,
    Region,
    StatNames,
    Stats,
    SuperContestCombos,
    SuperContestEffectProse,
    SuperContestEffects,
    TypeEfficacy,
    TypeGameIndices,
    TypeNames,
    Types,
    VersionGroupPokemonMoveMethods,
    VersionGroupRegions,
    VersionGroups,
    VersionNames,
    Versions,
]
