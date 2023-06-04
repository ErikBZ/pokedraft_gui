from rest_framework import serializers

from .models import *

class PokemonDraftListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonDraftList
        fields = ["name", "draft_id", "pokemon_ids"]
