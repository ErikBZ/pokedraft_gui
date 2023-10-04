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

class DraftPhase(models.TextChoices):
    PICK = 'P', _("Pick")
    BAN = 'B', _("Ban")


class DraftRules(models.Model):
    class TurnType(models.TextChoices):
        ROUND_ROBIN = 'RR', _('Round Robin')
        SNAKE = 'SN', _('Snake')

    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    picks_per_round = models.IntegerField(default=1)
    bans_per_round = models.IntegerField(default=1)
    max_pokemon = models.IntegerField(default=15)
    phase_start = models.CharField(
        max_length=1,
        choices=DraftPhase.choices,
        default=DraftPhase.BAN
    )
    turn_type = models.CharField(
        max_length=2,
        choices=TurnType.choices,
        default=TurnType.ROUND_ROBIN
    )

class DraftSession(models.Model):
    id= models.BigAutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    draft_set = models.ForeignKey(PokemonDraftSet, on_delete=models.CASCADE, null=True)
    min_num_players = models.IntegerField(default=2)
    max_num_players = models.IntegerField(default=4)
    banned_pokemon = models.ManyToManyField(Pokemon)
    draft_rules = models.ForeignKey(DraftRules, on_delete=models.CASCADE, null=True)
    current_player = models.TextField(null=True, blank=True)
    turn_ticker = models.IntegerField(default=0)
    accepting_players = models.BooleanField(default=True)
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
    key = models.TextField(default="secret")
    order_in_session = models.IntegerField(default=1)

    def is_current_turn(self):
        return self.session.current_player == self.id

    def to_json(self):
        return {
            "name": self.name,
            "current_turn": self.is_current_turn(),
            "order_in_session": self.order_in_session,
            "pokemon_selected": self.pokemon_selected,
            "id": self.id
        }
