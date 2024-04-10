import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from './components/home_view.vue'
import Connection_view from '@/components/connection_view.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/auth', component: Connection_view}
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router