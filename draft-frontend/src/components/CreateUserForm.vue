<template>
  <form @submit.prevent="handleSubmit">
    <label>Name: </label>
    <input type="text" v-model="name">
    <br>
    <p v-if="error">{{ error }}</p>
    <button type="submit">Join Session</button>
  </form>
</template>

<script>
export default {
  name: "CreateUserForm",
  data() {
    return {
      name: "",
      error: "",
    }
  },
  methods: {
    handleSubmit() {
      if(this.name === "") {
        this.error = "Name cannot be blank"
      }
      else {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },        
          body: JSON.stringify({name: this.name})
        }

        fetch("http://localhost:8000/draft_session/" + this.$route.params.id + "/create-user/", requestOptions)
          .then(res => res.json())
          .then(data => {
            if("message" in data){
              this.error = data["message"]
            }
          })
          .catch(err => console.log(err.message)
        )
      }
    }
  }
}
</script>
