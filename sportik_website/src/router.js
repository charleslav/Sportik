// router.js

import { createRouter, createWebHistory } from 'vue-router'

import Brand_view from '@/components/Brand View/brand_view.vue'
import Connection_view from '@/components/Connection view/login_view.vue'
import Register_view from '@/components/Connection view/register_view.vue'
import Monpanier_view from '@/components/Cart View/monpanier_view.vue'
import ItemModel_view from '@/components/Item View/itemModel_view.vue'
import informations_view from "@/components/View Infos/informations_view.vue"
import Brand_Model_View from '@/components/Brand Model View/brand_model_view.vue'
import Service_view from "@/components/service_view.vue"
import Contact_view from '@/components/contact_view.vue'
import Logout_Home from '@/components/Logout/logout_view.vue'
import Layout from '@/components/layout_basic.vue'
import Checkout_view from '@/components/checkout/checkout_view.vue'

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
      { path: "information/:brandModelId", component: informations_view, props: true},
      { path: "services", component: Service_view},
      { path: "contact", component: Contact_view},
      { path: "logout", component: Logout_Home},
      { path: "checkout", component: Checkout_view}
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
