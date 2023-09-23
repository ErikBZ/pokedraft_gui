from django.db import models
from django.utils.translation import gettext_lazy as _

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

class PokemonDraftSet(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    pokemon_list = models.ManyToManyField(Pokemon)

class DraftRules(models.Model):
    class TurnType(models.TextChoices):
        ROUND_ROBIN = 'RR', _('Round Robin')
        SNAKE = 'SN', _('Snake')

    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    picks_per_round = models.IntegerField(default=1)
    bans_per_round = models.IntegerField(default=1)
    max_pokemon = models.IntegerField(default=15)
    turn_type = models.CharField(
        max_length=2,
        choices=TurnType.choices,
        default=TurnType.ROUND_ROBIN
    )

class DraftSession(models.Model):
    class DraftPhase(models.TextChoices):
        PICK = 'P', _("Pick")
        BAN = 'B', _("Ban")

    id= models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    draft_set = models.ForeignKey(PokemonDraftSet, on_delete=models.CASCADE, null=True)
    min_num_players = models.IntegerField(default=2)
    max_num_players = models.IntegerField(default=4)
    banned_pokemon = models.ManyToManyField(Pokemon)
    draft_rules = models.ForeignKey(DraftRules, on_delete=models.CASCADE, null=True)
    current_phase = models.CharField(
        max_length=1,
        choices=DraftPhase.choices,
        default=DraftPhase.BAN
    )

class DraftUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    session = models.ForeignKey(DraftSession, on_delete=models.CASCADE, null=True)
    pokemon_selected = models.ManyToManyField(Pokemon)
    current_turn = models.BooleanField()
    key = models.TextField(default="secret")
    order_in_session = models.IntegerField(default=1)
