<template>
  <form @submit="handleSubmit">
    <label>Name:</label>
    <input v-model="name">
    <br>
    <label type="number">Maximum Players:</label>
    <input v-model="max_players">
    <br>
    <label type="number">Minimum Players:</label>
    <input v-model="min_players">
    <br>
    <select v-model="rule_id">
      <option value="">Create New</option>
      <option v-for="rule in rules" :value="rule.id" :key="rule.id">{{ rule.name }}</option>
    </select>
    <br>
    <select v-model="draft_id">
      <option v-for="set in draft_sets" :value="set.id" :key="set.id">{{ set.name }}</option>
    </select>
    <br>
    <button type="submit">Create Draft</button>
  </form>
</template>

<script>
export default {
  name: 'DraftSessionForm',
  data() {
    return {
      rules: [],
      draft_sets: [],
      name: "",
      min_players: 2,
      max_players: 4,
      rule_id: null,
      draft_id: null,
      draft_session: 0
    }
  },
  mounted() {
    fetch('http://localhost:8000/draft_rules/')
      .then(res => res.json())
      .then(data => this.rules = data)
      .catch(err => console.log(err.message))
    fetch('http://localhost:8000/draft_set/')
      .then(res => res.json())
      .then(data => this.draft_sets = data)
      .catch(err => console.log(err.message))
  },
  methods: {
    handleSubmit() {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },        
        body: JSON.stringify(
          {
            name: this.name,
            draft_set: this.draft_id,
            draft_rules: this.rule_id,
            min_num_players: this.min_players,
            max_num_players: this.max_players
          }
        )
      }
      fetch("http://localhost:8000/draft_session/", requestOptions)
        .then(res => res.json())
        .then(data => this.draft_session = data['id'])
        .catch(err => console.log(err.message))

        this.$router.push({path: "/draft_sesson/" + this.draft_session})
    }
  }
}
</script>