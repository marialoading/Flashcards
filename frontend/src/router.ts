import { createRouter, createWebHistory } from 'vue-router'
import Auth from './components/Auth.vue'
import Dashboard from './views/Dashboard.vue'
import Deck from './views/Deck.vue'
import Study from './views/Study.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/login', component: Auth },
  { path: '/register', component: Auth },
  { path: '/deck/:id', component: Deck },
  { path: '/deck/:id/study', component: Study }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router