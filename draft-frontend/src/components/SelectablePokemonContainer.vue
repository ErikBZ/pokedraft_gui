<template>
  <div class="lockin">
    Selected Pokemon: {{ selected_pokemon.name }}
    <button type="Submit" @click="sendPokemonSelection">Lock In</button>
  </div>
  <div class="modal-container">
    <div v-for="pk in pokemon" :key="pk.id" class="card">
      <p>{{ pk.name }}</p>
      <div>
        <p v-if="pk.type2">{{ pk.type1 }} / {{ pk.type2 }}</p>
        <p v-else>{{ pk.type1 }}</p>
      </div>
      <p v-if="banned_pokemon.includes(pk)">Banned</p>
      <a :href="'https://pokemondb.net/pokedex/' + pk.name" target="_blank" rel="noopener noreferrer">Pokedex</a>
      <br>
      <button @click="this.updateSelectedPokemon(pk)">Select</button>
    </div>
  </div>
</template>

<script>
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
    width: 90;
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