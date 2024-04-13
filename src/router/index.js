import { createRouter, createWebHashHistory } from 'vue-router'
import DraftSetList from '../views/DraftSetList.vue'
import DraftSetDetail from '../views/DraftSetDetail.vue'
import CreateDraftSession from '../views/Draft/CreateDraftSession.vue'
import DraftSession from '../views/Draft/DraftSession.vue'

const routes = [
  {
    path: '/draft_set',
    name: 'select_draft_set',
    component: DraftSetList
  },
  {
    path: '/draft_set/:id',
    name: "view_draft_set",
    component: DraftSetDetail
  },
  {
    path: '/create_draft_session',
    name: "create_draft_session",
    component: CreateDraftSession
  },
  {
    path: '/draft_session/:id',
    name: "draft_session",
    component: DraftSession
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
