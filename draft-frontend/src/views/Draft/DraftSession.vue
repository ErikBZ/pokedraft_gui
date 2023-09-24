<template>
  <h1>Draft Session: {{ name }}</h1>
  <CreateUserForm v-if="!user_logged_in"/>
  <div v-else>
    <p>You've Logged In!</p>
  </div>

  <div v-if="draft_set">
    <div v-for="pk in draft_set.pokemon_list" :key="pk.id">
      {{ pk.name }}
    </div>
  </div>
</template>

<script>
import CreateUserForm from '@/components/CreateUserForm.vue';
export default {
  name: "DraftSetList",
  components: { CreateUserForm },
  data() {
    return {
      name: "",
      min_num_players: 0,
      max_num_players: 0,
      current_phase: "",
      banned_pokemon: [],
      user_logged_in: false,
      draft_set: null,
      draft_rules: null
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

        return Promise.all([
          fetch('http://localhost:8000/draft_set/' + draft_set_id).then(res => res.ok && res.json()),
          fetch('http://localhost:8000/draft_rules/' + draft_rules_id).then(res => res.ok && res.json()),
        ])
      })
      .then(data => {
        this.draft_set = data[0]
        this.draft_rules = data[1]
      })
      .catch(err => console.log(err.message))
  }
}
</script>
