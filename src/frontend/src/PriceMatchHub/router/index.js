import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import Main from "@/PriceMatchHub/components/main.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/PriceMatchHub'
        },
        {
            path: '/PriceMatchHub',
            component: Main,
        }
    ]
})

export default router