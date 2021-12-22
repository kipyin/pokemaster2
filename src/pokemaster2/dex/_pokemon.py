"""Pokemon class for `dex` module."""

import os

from ..db import get
from . import resource_path
from .exceptions import *


class Pokemon(object):
    def __init__(self, pokemon, language=get.DEFAULT_LANGUAGE, version=get.DEFAULT_VERSION):
        try:
            self.number = pokemon
            results = get.pokedex_entry(self.number, language=language, version=version)
            # if len(results) == 0:
            #     # TODO: Separate exception for "No entry for this version/language combo"
            #     raise NoSuchPokemon(pokemon)
        except NoSuchPokemon:
            self.number = 0
            self.name = "MISSINGNO."
            self.genus = "???"
            self.flavor = "Pokémon %s not found" % pokemon
            self.types = ["flying", "normal"]
            self.chain = {(0, "MISSINGNO."): {}}
            self.height = 10
            self.weight = 100
        else:
            entry = results
            self.number = entry.species_id
            self.name = entry.name
            self.genus = entry.genus
            self.flavor = entry.flavor_text.replace("\n", " ").replace("\f", " ")
            self.types = get.pokemon_types(self.number)
            self.chain = get.pokemon_evolution_chain(self.number, language=language)
            self.height = entry.height
            self.weight = entry.weight

    def icon(self, shiny=False, mega=0):
        mega_suffix = ["", "_mega", "_mega_1"][mega]
        return "icons/icon%03d%s%s.png" % (self.number, "s" if shiny else "", mega_suffix)

    @property
    def mega(self):
        if os.path.isfile(os.path.join(resource_path, self.icon(mega=2))):
            return 2
        if os.path.isfile(os.path.join(resource_path, self.icon(mega=1))):
            return 1
        return 0
