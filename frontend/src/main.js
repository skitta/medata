import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from './store'

const app = createApp(App)

app.config.globalProperties.$http = axios

axios.defaults.baseURL = 'http://127.0.0.1:8000/api'

app.use(store).use(router).mount('#app')
