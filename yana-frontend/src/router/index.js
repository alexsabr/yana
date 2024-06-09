import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'Main Page',
    component: HomeView
  },
  {
    path: '/newsrefresher',
    name: 'News Refresher',
    component: () => import('../views/NewsRefresh.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
