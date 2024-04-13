import { createApp } from 'vue'
import App from './App.vue'
import { VueCookies } from 'vue-cookies'
import router from './router'

const app = createApp(App)
app.use(router)
app.use(VueCookies)
app.mount('#app')
