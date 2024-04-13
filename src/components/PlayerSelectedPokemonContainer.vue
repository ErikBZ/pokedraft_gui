<template>
  <p>{{ name }}</p>
  <div class="player-modal-container">
    <div v-for="pk in pokemon" :key="pk.id" class="player-card">
      <p>{{ pk.name }}</p>
      <div>
        <p v-if="pk.type2">{{ pk.type1 }} / {{ pk.type2 }}</p>
        <p v-else>{{ pk.type1 }}</p>
      </div>
      <a :href="'https://pokemondb.net/pokedex/' + pk.name" target="_blank" rel="noopener noreferrer">Pokedex</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "PlayerSelectedPokemonContainer",
  props: {
    name: String,
    pokemon: Array,
  },
}
</script>

<style>
  .player-modal-container {
    margin: auto;
    overflow: scroll;
    border: 5px solid black;
    background-color: rgba(200,200,200,1);
  }
  .player-card {
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    margin: 10px;
    display: inline-block;
    height: 150px;
    width: 120px;
    background-color: rgba(255,255,255,1);
    font-size: 14px;
  }
  .card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  }
  .card button {
    margin-top: 40px;
  }
</style>

