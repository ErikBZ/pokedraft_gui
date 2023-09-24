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
    setDraftPlayerCookie(draft_player) {
      const sesion_id = draft_player['session_id']
      var draft_sessions = {}
      if(window.$cookies.isKey("draft_sessions")) {
        const ds_raw = window.$cookies.get("draft_sessions")
        draft_sessions = JSON.parse(atob(ds_raw))
      }

      draft_sessions[sesion_id] = draft_player
      const ds_cookie = btoa(JSON.stringify(draft_sessions))
      console.log("Gonna set a cookie")
      console.log(ds_cookie)
      window.$cookies.set("draft_sessions", ds_cookie)
    },
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
            } else {
              this.setDraftPlayerCookie(data)
            }
          })
          .catch(err => console.log(err.message)
        )
      }
    }
  }
}
</script>
