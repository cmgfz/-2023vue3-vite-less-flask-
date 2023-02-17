import {createApp} from 'vue'
import Router from './router/index.js'
import Store from './store'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './mock/mockServer'//加载mockServer即可
import VueLazyload from 'vue-lazyload'
import loading from './common/imgs/loading.gif'
const app=createApp(App);
app.use(Router)
app.use(Store)
app.use(ElementPlus)
app.use(VueLazyload,{//内部自定义了一个指令lazy
    loading
})
app.mount('#app')