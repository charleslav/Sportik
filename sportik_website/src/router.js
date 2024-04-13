// router.js

import { createRouter, createWebHistory } from 'vue-router'

import Brand_view from '@/components/Brand View/brand_view.vue'
import Connection_view from '@/components/Connection view/login_view.vue'
import Register_view from '@/components/Connection view/register_view.vue'
import Monpanier_view from '@/components/monpanier_view.vue'
import ItemModel_view from '@/components/Item View/itemModel_view.vue'
import informations_view from "@/components/View Infos/informations_view.vue"
import Brand_Model_View from '@/components/Brand Model View/brand_model_view.vue'
import Layout from '@/components/layout.vue'

const routes = [
  {
    path : "/",
    component: Layout,
    children: [
      { path: '', component: Brand_view },
      { path: 'login', component: Connection_view },
      { path: 'register', component: Register_view},
      { path: "cart", component: Monpanier_view},
      { path: "item/:itemId", component: ItemModel_view, props: true},
      { path: "brand_model/:brandId", component: Brand_Model_View, props: true},
      { path: "brand_model/:brandId", component: informations_view, props: true}
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
