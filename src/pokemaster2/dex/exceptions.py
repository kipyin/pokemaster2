"""Dex exceptions."""


class NoSuchPokemon(Exception):
    def __init__(self, pokemon):
        super(NoSuchPokemon, self).__init__("Pokémon %s not found" % pokemon)
