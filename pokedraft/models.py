from django.db import models

class PokemonDraftList(models.Model):
    draft_id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    pokemon_ids = models.TextField(null=True)
