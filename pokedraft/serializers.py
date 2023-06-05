from rest_framework import serializers

from .models import *

class PokemonDraftListSerializer(serializers.HyperlinkedModelSerializer):
    pokemon_list = serializers.ListField(child=serializers.IntegerField())
    class Meta:
        model = PokemonDraftList
        read_only_fields = ['draft_id', "pokemon_list"]
        fields = ["name", "draft_id", "pokemon_list"]

    def to_representation(self, instance):
        instance.pokemon_list = [int(i) for  i in instance.pokemon_ids.split(',')]
        return super(PokemonDraftListSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        ret = super(PokemonDraftListSerializer, self).to_internal_value(data)
        if ret["pokemon_list"]:
            ret["pokemon_ids"] = ",".join(str(i) for i in ret["pokemon_list"])
        del ret["pokemon_list"]
        return ret
