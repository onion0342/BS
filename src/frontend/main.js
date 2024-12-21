import './assets/main.css'
import axios from 'axios'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import App from './app.vue'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { sha256 } from "js-sha256";

import { createRouter, createWebHistory} from 'vue-router'
import User from "./src/login/components/user.vue";
import Signup from "./src/login/components/signup.vue";
import Main from "./src/PriceMatchHub/components/main.vue";
import UserCenter from "./src/PriceMatchHub/components/userCenter.vue"
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            redirect: '/login/user',
        },
        {
            path: '/login/user',
            component: User,
        },
        {
            path: '/login/signup',
            component: Signup,
        },
        {
            path: '/PriceMatchHub',
            redirect: '/PriceMatchHub/main',
        },
        {
            path: '/PriceMatchHub/main',
            component: Main,
        },
        {
            path: '/PriceMatchHub/usercenter',
            component: UserCenter,
        },
    ]
})

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
axios.defaults.baseURL = 'http://localhost:8000';
app.config.globalProperties.$sha256 = sha256;
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')

