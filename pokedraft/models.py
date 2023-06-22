from django.db import models

TYPES = [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic", "bug",
    "rock", "ghost", "dragon", "dark", "steel", "fairy"
]

class Pokemon(models.Model):
    name = models.TextField(null=True, blank=True)
    type1 = models.TextField(null=True, blank=True)
    type2 = models.TextField(null=True, blank=True)
    evolves_from = models.TextField(null=True, blank=True)
    gen = models.IntegerField()
    is_legendary = models.BooleanField()
    is_mythic = models.BooleanField()

class PokemonDraftList(models.Model):
    draft_id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    pokemon_list = models.ManyToManyField(Pokemon)
