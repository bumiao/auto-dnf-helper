import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'vxe-table/lib/style.css'

import '@/style/index.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
