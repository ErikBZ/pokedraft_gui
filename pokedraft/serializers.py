from rest_framework import serializers

from .models import *

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        read_only_fields = ["id", "name", "type1", "type2", "evolves_from", "gen", "is_legendary", "is_mythic"]
        fields = ["id", "name", "type1", "type2", "evolves_from", "gen", "is_legendary", "is_mythic"]

class PokemonDraftListSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonDraftList
        fields = ["name", "draft_id"]

class PokemonDraftListSerializer(serializers.HyperlinkedModelSerializer):
    pokemon_list = PokemonSerializer(many=True)
    class Meta:
        model = PokemonDraftList
        read_only_fields = ['draft_id', 'pokemon_list']
        fields = ["name", "draft_id", "pokemon_list"]

class DraftSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftSession
        fields = ["name", "draft_used", "max_pokemon", "session_id"]

class DraftUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DraftUser
        fields = ["name", "session_id", "current_turn", "pokemon_selected"]
