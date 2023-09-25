<template>
  <h1>Draft Session: {{ name }}</h1>
  <CreateUserForm v-if="!user_logged_in"/>
  <div v-else>
    <p>{{ draft_user['name'] }}</p>
  </div>
  <SelectablePokemonContainer :pokemon="pokemon" :draft_user="draft_user" v-if="draftUserLoaded"/>
</template>

<script>
import CreateUserForm from '@/components/CreateUserForm.vue';
import SelectablePokemonContainer from '@/components/SelectablePokemonContainer.vue';
export default {
  name: "DraftSetList",
  components: { CreateUserForm, SelectablePokemonContainer },
  data() {
    return {
      name: "",
      min_num_players: 0,
      max_num_players: 0,
      current_phase: "",
      banned_pokemon: [],
      user_logged_in: false,
      draft_set: null,
      draft_rules: null,
      draft_user: null,
      pokemon: []
    }
  },
  computed: {
    draftUserLoaded() {
      return this.draft_user !== null
    }
  },
  mounted() {
    const ds_req = fetch('http://localhost:8000/draft_session/' + this.$route.params.id)
      .then(res => res.json())
    
    ds_req.then(data => {
        const draft_set_id = data['draft_set']
        const draft_rules_id = data['draft_rules']
        this.name = data['name'],
        this.min_num_players = data['min_num_players'],
        this.max_num_players = data['max_num_players'],
        this.current_phase = data['current_phase'],
        this.banned_pokemon = data['banned_pokemon']

        this.loadDraftUserCookie(this.$route.params.id)

        return Promise.all([
          fetch('http://localhost:8000/draft_set/' + draft_set_id).then(res => res.ok && res.json()),
          fetch('http://localhost:8000/draft_rules/' + draft_rules_id).then(res => res.ok && res.json()),
        ])
      })
      .then(data => {
        this.draft_set = data[0]
        this.pokemon = this.draft_set['pokemon_list']
        this.draft_rules = data[1]
      })
      .catch(err => console.log(err.message))
  },
  methods: {
    loadDraftUserCookie(draft_session_id){
      if(window.$cookies.isKey("draft_sessions")){
        const raw_sessions = window.$cookies.get("draft_sessions")
        const sessions = JSON.parse(atob(raw_sessions))
        this.draft_user = sessions[draft_session_id]
        if(this.draft_user){
          this.user_logged_in = true
        }
      }
    }
  }
}
</script>
