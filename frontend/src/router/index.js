import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: { title: '仪表盘', icon: 'dashboard' },
    children: [{
      path: 'capacityManagement',
      name: 'CapacityManagement',
      component: () => import('@/views/capacityManagement/index'),
      meta: { title: '容量管理' }
    },{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '动态阈值告警' }
    }]
  },

  {
    path: '/',
    component: Layout,
    redirect: '/aboutUs',
    children: [{
        path: 'aboutUs',
        name: 'AboutUs',
        component: () => import('@/views/aboutUs/index'),
        meta: { title: '关于我们', icon: 'message' }
      }]
  },
  
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
