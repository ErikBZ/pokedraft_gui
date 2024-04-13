<template>
  <h1>Draft Set</h1>
  <div v-for="set in draft_sets" :key="set.id" class="set">
    <a :href="'/#/draft_set/' + set.id.id.String">{{ set.name }}</a>
  </div>
</template>

<script>
export default {
  name: "DraftSetList",
  data() {
    return {
      draft_sets: []
    }
  },
  mounted() {
    fetch(process.env.VUE_APP_BACKEND +'/draft_set/')
      .then(res => res.json())
      .then(data => this.draft_sets = data)
      .catch(err => console.log(err.message))
  }
}
</script>
