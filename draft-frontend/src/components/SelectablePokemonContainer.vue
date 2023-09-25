<template>
  <div class="lockin">
    Selected Pokemon: {{ selected_pokemon.name }}
    <button type="Submit" @click="sendPokemonSelection">Lock In</button>
  </div>
  <div class="modal-container">
    <div v-for="pk in pokemon" :key="pk.id" class="card">
      <p>{{ pk.name }}</p>
      <div v-if="pk.type2">
        <p>{{ pk.type1 }} / {{ pk.type2 }}</p>
      </div>
      <div v-else>
        <p>{{ pk.type1 }}</p>
      </div>
      <a :href="'https://pokemondb.net/pokedex/' + pk.name" target="_blank" rel="noopener noreferrer">Pokedex</a>
      <br>
      <button @click="this.updateSelectedPokemon(pk)">Select</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "SelectablePokemonContainer",
  props: {
    pokemon: Array,
    draft_user: Object,
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
      console.log(this.draft_user)
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },        
        body: JSON.stringify({
          "pokemon_id": this.selected_pokemon.id,
          "secret": this.draft_user.key,
          "action": "P",
          "user_id": this.draft_user.user_id,
        })
      }

      fetch("http://localhost:8000/draft_session/" + this.$route.params.id + "/select-pokemon/", requestOptions)
        .then(res => res.json())
        .then(data => {
          console.log(data)
        })
        .catch(err => console.log(err.message))
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