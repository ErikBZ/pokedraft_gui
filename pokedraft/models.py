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

class DraftSession(models.Model):
    session_id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    draft_used = models.ForeignKey(PokemonDraftList, on_delete=models.CASCADE, null=True)
    max_pokemon = models.IntegerField()
    min_num_players = models.IntegerField(default=2)
    max_num_players = models.IntegerField(default=4)
    current_phase = models.TextField(default="select")
    banned_pokemon = models.ManyToManyField(Pokemon)
    starting_player = models.TextField(null=True, blank=True)

class DraftUser(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    session_id = models.ForeignKey(DraftSession, on_delete=models.CASCADE, null=True)
    pokemon_selected = models.ManyToManyField(Pokemon)
    current_turn = models.BooleanField()
    key = models.TextField(default="secret")
    # for the actual draft
    next = models.TextField(null=True, blank=True)
    prev = models.TextField(null=True, blank=True)
