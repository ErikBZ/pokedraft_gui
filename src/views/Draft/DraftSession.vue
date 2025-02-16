<template>
  <h1>Draft Session: {{ name }}</h1>
  <CreateUserForm v-if="!user_logged_in"/>
  <div v-else>
    <p>{{ draft_user['name'] }}</p>
  </div>
  <p>Current Player's Turn: {{ current_player }}</p>
  <p>Current Phase: {{ long_name_phase }}</p>
  <SelectablePokemonContainer @select-pokemon="selectPokemon" :pokemon="pokemon" :banned_pokemon="banned_pokemon" :draft_user="draft_user" v-if="draftUserLoaded"/>
  <br>
  <div class="player-container">
    <div v-for="player in players" :key="player.name" class="player-item">
      <PlayerSelectedPokemonContainer :pokemon="player.pokemon" :name="player.name"/>
    </div>
  </div>
</template>

<script>
import CreateUserForm from '@/components/CreateUserForm.vue';
import SelectablePokemonContainer from '@/components/SelectablePokemonContainer.vue';
import PlayerSelectedPokemonContainer from '@/components/PlayerSelectedPokemonContainer.vue';
import get_id from '@/utils/utilities.js'
export default {
  name: "DraftSetList",
  components: { CreateUserForm, SelectablePokemonContainer, PlayerSelectedPokemonContainer },
  data() {
    return {
      name: "",
      min_num_players: 0,
      max_num_players: 0,
      current_phase: "",
      current_player: "",
      banned_pokemon: [],
      user_logged_in: false,
      draft_set: null,
      draft_rules: null,
      draft_user: null,
      players: {},
      pokemon: []
    }
  },
  computed: {
    draftUserLoaded() {
      return this.draft_user !== null
    },
    long_name_phase() {
      if(this.current_phase === "B") {
        return "Banning"
      }
      else {
        return "Picking"
      }
    }
  },
  mounted() {
    console.log(process.env.VUE_APP_BACKEND + '/draft_session/' + this.$route.params.id)

    const ds_req = fetch(process.env.VUE_APP_BACKEND + '/draft_session/' + this.$route.params.id)
      .then(res => res.json())
    
    ds_req.then(data => {
        const draft_set_id = data['draft_set']
        console.log(data['draft_rules'])
        const draft_rules_id = get_id(data['draft_rules'])
        this.name = data['name'],
        this.min_num_players = data['min_num_players'],
        this.max_num_players = data['max_num_players'],
        this.banned_pokemon = data['selected_pokemon']
        this.current_phase = data['current_phase'],

        this.loadDraftUserCookie(this.$route.params.id)

        return Promise.all([
          fetch(process.env.VUE_APP_BACKEND + '/draft_set/' + draft_set_id + "?detailed=true").then(res => res.ok && res.json()),
          fetch(process.env.VUE_APP_BACKEND + '/draft_rules/' + draft_rules_id).then(res => res.ok && res.json()),
        ])
      })
      .then(data => {
        this.draft_set = data[0]
        this.pokemon = this.draft_set['pokemon']['Stats']
        console.log(this.pokemon)
        this.draft_rules = data[1]
      })
      .catch(err => console.log(err.message))
      this.fetch_session_data()
  },
  beforeCreate: function() {
    this.ticker = setInterval(() => {
      this.fetch_session_data() 
    }, 15000);
  },
  beforeUnmount: function() {
    clearInterval(this.ticker)
  },
  methods: {
    fetch_session_data() {
      fetch(process.env.VUE_APP_BACKEND + '/draft_session/' + this.$route.params.id + '/update')
        .then(res => res.json())
        .then(data => {
          this.current_phase = data['current_phase'],
          this.banned_pokemon = data['banned_pokemon']
          this.players = data['players']
          this.current_player = data['current_player']
        })
    },
    loadDraftUserCookie(draft_session_id){
      if(window.$cookies.isKey("draft_sessions")){
        const raw_sessions = window.$cookies.get("draft_sessions")
        const sessions = JSON.parse(atob(raw_sessions))
        this.draft_user = sessions[draft_session_id]
        if(this.draft_user){
          this.user_logged_in = true
        }
      }
    },
    selectPokemon(pokemon) {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          "pokemon_id": pokemon.dex_id,
          "secret": this.draft_user.key,
          "action": this.current_phase,
          "user_id": this.draft_user.user_id,
        })
      }

      fetch(process.env.VUE_APP_BACKEND + '/draft_session/' + this.$route.params.id + '/select-pokemon/', requestOptions)
        .then(res => res.json())
        .then(data => {
          if(data.isKey("phase")) {
            this.current_phase = data['phase']
            this.banned_pokemon = data['banned_pokemon']
          }
        })
        .catch(err => console.log(err.message))
    }
  }
}
</script>

<style>
  .player-container {
    width: 90%;
    margin: auto;
    border: 5px solid green;
    background-color: rgba(225,225,225,1);
  }
  .player-item {
    display: inline-block;
    width: 400px;
    margin: 10px
  }
</style>
