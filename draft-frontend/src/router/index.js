import { createRouter, createWebHashHistory } from 'vue-router'
import DraftSetList from '../views/DraftSetList.vue'
import DraftSetDetail from '../views/DraftSetDetail.vue'
import CreateDraftSession from '../views/Draft/CreateDraftSession.vue'

const routes = [
  {
    path: '/draft_set',
    name: 'Draft Set',
    component: DraftSetList
  },
  {
    path: '/draft_set/:id',
    name: "Draft Set Pokemon List",
    component: DraftSetDetail
  },
  {
    path: '/draft_session',
    name: "Create Draft Session",
    component: CreateDraftSession
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
