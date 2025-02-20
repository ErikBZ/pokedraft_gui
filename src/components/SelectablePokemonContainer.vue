<template>
  <div class="lockin">
    Selected Pokemon: {{ selected_pokemon.name }}
    <button type="Submit" @click="sendPokemonSelection">Lock In</button>
    <p>{{banned_pokemon}}</p>
  </div>
  <div class="modal-container">
    <div v-for="pk in pokemon" :key="pk.dex_id" class="card">
      <p>{{ pk.dex_id}}: {{pk.name }}</p>
      <div>
        <p v-if="pk.type2 != 'NONE'">{{ pk.type1 }} / {{ pk.type2 }}</p>
        <p v-else>{{ pk.type1 }}</p>
      </div>
      <a :href="'https://pokemondb.net/pokedex/' + pk.name" target="_blank" rel="noopener noreferrer">Pokedex</a>
      <br>
      <p v-if="isPokemonBanned(pk.id)">Banned or Selected</p>
      <button v-else @click="this.updateSelectedPokemon(pk)">Select</button>
    </div>
  </div>
</template>

<script>
import get_id from '@/utils/utilities.js'
export default {
  name: "SelectablePokemonContainer",
  emits: ["select-pokemon"],
  props: {
    pokemon: Array,
    banned_pokemon: Array
  },
  data() {
    return {
      selected_pokemon: ""
    }
  },
  methods: {
    isPokemonBanned(pk) {
      return this.banned_pokemon.includes(parseInt(get_id(pk)))
    },
    updateSelectedPokemon(pk) {
      this.selected_pokemon = pk
    },
    sendPokemonSelection() {
      if(this.selected_pokemon === null) {
        return
      }
      this.$emit("select-pokemon", this.selected_pokemon)
    }
  }
}
</script>

<style>
  .lockin {
    height: 50px;
  }
  .lockin button {
    height: 40px;
    width: 90px;
    float: right;
    margin-right: 30%;
  }
  .modal-container {
    width: 80%;
    height: 600px;
    margin: auto;
    overflow: scroll;
    border: 5px solid black;
    background-color: rgba(200,200,200,1);
  }
  .card {
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    margin: 10px;
    display: inline-block;
    height: 300px;
    width: 240px;
    background-color: rgba(255,255,255,1);
  }
  .card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
  .card button {
    margin-top: 40px;
  }
</style>
