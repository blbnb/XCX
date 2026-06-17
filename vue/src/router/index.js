import { createRouter, createWebHistory } from 'vue-router'
import BookList from '../views/BookList.vue'
import BookAdd from '../views/BookAdd.vue'
import Login from '../views/Login.vue'
import Orders from '../views/Orders.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'BookList',
    component: BookList,
    meta: { requiresAuth: true }
  },
  {
    path: '/add',
    name: 'BookAdd',
    component: BookAdd,
    meta: { requiresAuth: true }
  },
  {
    path: '/edit/:id',
    name: 'BookEdit',
    component: BookAdd,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: Orders,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
