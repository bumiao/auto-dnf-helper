import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('@/layout/index.vue'),
      redirect: { name: 'AutoUnpack' },
      children: [
        {
          path: 'introduction',
          name: 'Introduction',
          component: () => import('@/views/introduction.vue')
        },
        {
          path: 'auto-unpack',
          name: 'AutoUnpack',
          component: () => import('@/views/auto-unpack.vue')
        }
      ]
    }
  ]
})

export default router
