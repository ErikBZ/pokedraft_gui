from pokedraft.models import Pokemon, PokemonDraftSet
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
    PokemonDraftSet.objects.all().delete()

def clear_pokemon():
    Pokemon.objects.all().delete()

def build_lists():
    draft_sets = [x.name for x in PokemonDraftSet.objects.all()]

    for gen in range(1,8):
        base_name = f"Gen {gen} All"
        if base_name not in draft_sets:
            build_list(base_name, gen)

        name_no_legends = f"{base_name} No Legends"
        if name_no_legends not in draft_sets:
            build_list(name_no_legends, gen, with_legends=False)

        name_base_forms = f"{base_name} NL Base Forms"
        if name_base_forms not in draft_sets:
            build_list(name_base_forms, gen, with_legends=False, only_base_forms=True)


def build_list(name, gen, with_legends=True, only_base_forms=False):
    pokemon = Pokemon.objects.all()
    draft_set = PokemonDraftSet(name=name)
    draft_set.save()

    pokemon = at_least_gen(pokemon, gen)
    if not with_legends:
        pokemon = no_legends(pokemon)
    if only_base_forms:
        pokemon = filter_to_base_forms(pokemon)

    print(f"Creating draft set: {name}")
    draft_set.pokemon_list.add(*pokemon)

# this will not work for gens 8 or 9
def at_least_gen(queryset, generation):
    return queryset.filter(gen__lte=generation)

def no_legends(queryset):
    return queryset.filter(is_mythic=False, is_legendary=False)

def filter_to_base_forms(queryset):
    return queryset.filter(evolves_from="")
