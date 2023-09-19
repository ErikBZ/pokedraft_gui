#!/usr/bin/env python3
import csv
import json

TYPES = [
    "normal", "fighting", "flying", "poison", "ground", "rock",
    "bug", "ghost", "steel", "fire", "water", "grass",
    "electric", "psychic", "ice", "dragon", "dark", "fairy"
]

def main():
    dump_species()
    add_types()

def add_types():
    pokemon = []
    pokemon_typing = {}
    with open("./data/pokemon_models.json") as f:
        pokemon = json.load(f)

    with open("./data/pokemon_types.csv") as f:
        ps_reader = csv.DictReader(f)
        for ps in ps_reader:
            p_id = ps["pokemon_id"]
            t_id = int(ps["type_id"]) - 1
            if not p_id in pokemon_typing:
                pokemon_typing[p_id] = {"type1": TYPES[t_id]}
            else:
                pokemon_typing[p_id]["type2"] = TYPES[t_id]

    for pk in pokemon:
        pk_type = pokemon_typing[pk["id"]]
        pk["type1"] = pk_type["type1"]
        pk["type2"] = pk_type["type2"] if "type2" in pk_type else ""

    with open("./data/pokemon_models.json", "w") as f:
        json.dump(pokemon, f)

def dump_species():
    pokemon = []
    with open("./data/pokemon_species.csv") as f:
        ps_reader = csv.DictReader(f)
        for ps in ps_reader:
            data  = {}
            data["id"] = ps["id"]
            data["name"] = ps["identifier"]
            data["is_mythical"] = int(ps["is_mythical"]) == 1
            data["is_legendary"] = int(ps["is_legendary"]) == 1
            data["gen"] = ps["generation_id"]
            data["evolves_from"] = ps["evolves_from_species_id"]
            pokemon.append(data)
    
    with open("./data/pokemon_models.json", "w") as f:
        json.dump(pokemon, f)


if __name__ == "__main__":
    main()
