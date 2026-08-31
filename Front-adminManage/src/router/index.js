import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/users',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'users',
        name: 'users',
        component: () => import('../views/UserManage.vue'),
        meta: { title: '用户管理', requiresAuth: true },
      },
      {
        path: 'articles',
        name: 'articles',
        component: () => import('../views/ArticleManage.vue'),
        meta: { title: '文章列表', requiresAuth: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - 后台管理系统` : '后台管理系统'
  const token = localStorage.getItem('admin_token')
  if (to.meta.requiresAuth && !token) {
    return { name: 'login' }
  }
  if (to.name === 'login' && token) {
    return { name: 'users' }
  }
})

export default router
