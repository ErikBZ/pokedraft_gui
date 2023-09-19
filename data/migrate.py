from pokedraft.models import Pokemon, PokemonDraftList
from django.db import connection
import json

def get_json(file):
    with open(file) as f:
        return json.load(f)

def build_pokemon():
    pokemon = get_json("./data/pokemon_models.json")
    batch = []

    for pk in pokemon:
        pk_mod = to_model(pk)
        batch.append(pk_mod)
        if len(batch) > 200:
            Pokemon.objects.bulk_create(batch)
            batch = []

def to_model(data):
    return Pokemon(id=int(data["id"]), name=data["name"], type1=data['type1'],
                   type2=data["type2"], evolves_from=data["evolves_from"],
                   gen=int(data["gen"]), is_legendary=bool(data["is_legendary"]),
                   is_mythic=bool(data["is_mythical"]))

def build():
    build_pokemon()

def clear_list():
    PokemonDraftList.objects.all().delete()

def clear_pokemon():
    Pokemon.objects.all().delete()

def build_lists():
    all_pokemon = Pokemon.objects.all()
    list_gen_1 = PokemonDraftList(name="Generation 1 All")
    list_gen_1.save()
    print("Adding pokemon to the list")
    list_gen_1.pokemon_list.add(*at_least_gen(all_pokemon, 1))
    print("Added!")

# this will not work for gens 8 or 9
def at_least_gen(queryset, generation):
    return queryset.filter(gen__lte=generation)

def no_legends(queryset):
    return queryset.filter(is_mythical=False, is_legendary=False)
