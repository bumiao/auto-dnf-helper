import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'virtual:uno.css'

import '@/style/index.css'
// import '@/utils/rem'

const app = createApp(App)

app.use(router)

app.mount('#app')
