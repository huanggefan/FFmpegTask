import Vue from 'vue'

Vue.config.productionTip = false

/******************************************************************************/

import "amfe-flexible"

/******************************************************************************/

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)

/******************************************************************************/

import '@/style/all.css'

/******************************************************************************/

import App from '@/App.vue'
import router from '@/router'
import store from '@/store'

new Vue({
    router,
    store,
    render: function (h) {
        return h(App)
    }
}).$mount(`#app`)
