import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: `/`,
        name: `home`,
        redirect: `/new`
    },
    {
        path: `/new`,
        name: `NewView`,
        component: () => {
            return import(`@/views/NewView.vue`)
        }
    },
    {
        path: `/list`,
        name: `ListView`,
        component: () => {
            return import(`@/views/ListView.vue`)
        }
    },
]

const router = new VueRouter({
    routes
})

router.beforeEach((to, from, next) => {
    if (to.path !== from.path) {
        next()
    }
})

export default router
