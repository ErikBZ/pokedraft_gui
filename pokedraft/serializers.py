from rest_framework import serializers

from .models import *

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        read_only_fields = ["name", "type1", "type2", "evolves_from", "gen", "is_legendary", "is_mythic"]
        fields = ["name", "type1", "type2", "evolves_from", "gen", "is_legendary", "is_mythic"]

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

