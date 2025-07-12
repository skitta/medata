import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { setupErrorHandler } from './plugins/errorHandler'
import 'ant-design-vue/dist/reset.css';

const app = createApp(App)

setupErrorHandler(app)
app.use(createPinia()).use(router).mount('#app')