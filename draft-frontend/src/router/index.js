import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DraftSetList from '../views/DraftSetList.vue'
import DraftSetDetail from '../views/DraftSetDetail.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/draft_set',
    name: 'Draft Set',
    component: DraftSetList
  },
  {
    path: '/draft_set/:id',
    name: "Draft Set Pokemon List",
    component: DraftSetDetail
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
