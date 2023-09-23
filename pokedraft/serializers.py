from rest_framework import serializers

from .models import *

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        read_only_fields = ["id", "name", "type1", "type2", "evolves_from", "gen", "is_legendary", "is_mythic"]
        fields = ["id", "name", "type1", "type2", "evolves_from", "gen", "is_legendary", "is_mythic"]

class PokemonDraftSetSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonDraftSet
        fields = ["name", "id"]

class PokemonDraftSetSerializer(serializers.HyperlinkedModelSerializer):
    pokemon_list = PokemonSerializer(many=True)
    class Meta:
        model = PokemonDraftSet
        read_only_fields = ['id', 'pokemon_list']
        fields = ["name", "id", "pokemon_list"]

class DraftRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftRules
        fields = ["name", "id", "picks_per_round", "bans_per_round", "turn_type", "max_pokemon"]

class DraftSessionSerializer(serializers.ModelSerializer):
    players = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = DraftSession
        read_only_fields = ["banned_pokemon", "id", "current_phase"]
        exclude = []

class DraftUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DraftUser
        fields = ["name", "id", "current_turn", "pokemon_selected"]
