<template>
  <h1>Pokemon</h1>
  <h2>{{ name }}</h2>
  <li v-for="pk in pokemon" :key="pk.name">
    {{ pk.name }}
  </li>
</template>

<script>
export default {
  name: 'DraftSetDetail',
  data() {
    return {
      name: "",
      draft_id: 0,
      pokemon: [],
    }
  },
  mounted() {
    fetch('http://localhost:8000/draft_set/' + this.$route.params.id)
      .then(res => res.json())
      .then(data => {
        this.name = data['name'],
        this.draft_id = data['id'],
        this.pokemon = data['pokemon_list']
      })
      .catch(err => console.log(err.message))
  }
}
</script>
