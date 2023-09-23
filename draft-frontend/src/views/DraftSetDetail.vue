<template>
  <h1>Pokemon</h1>
</template>

<script>
export default {
  name: 'DraftSetDetail',
  data() {
    return {
      name: "",
      draft_id: 0,
      pokemon: []
    }
  },
  mounted() {
    fetch('http://localhost:8000/drafts_list/1')
      .then(res => res.json())
      .then(data => this.name = data['name'])
      .then(data => this.draft_id = data['draft_id'])
      .then(data => this.pokemon = data['pokemon'])
      .catch(err => console.log(err.message))
  }
}
</script>
