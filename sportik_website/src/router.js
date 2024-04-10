import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from './components/Home/home_view.vue'
import Connection_view from '@/components/connection_view.vue'
import Register_view from '@/components/register_view.vue'
import Monpanier_view from '@/components/monpanier_view.vue'
import ItemModel_view from '@/components/itemModel_view.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: Connection_view },
  { path: '/register', component: Register_view},
  { path: "/cart", component: Monpanier_view},
  { path: "/item", component: ItemModel_view}
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router