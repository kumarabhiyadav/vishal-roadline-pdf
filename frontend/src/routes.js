import { createRouter, createWebHashHistory } from 'vue-router'
import Home from './Home.vue'
import Invoices from './Invoices.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home, // Make Home the landing page
  },
  {
    path: '/invoices',
    name: 'Invoices',
    component: Invoices,
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
