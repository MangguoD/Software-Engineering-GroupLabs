// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

// 设置Axios的基础URL指向后端服务地址
axios.defaults.baseURL = 'http://localhost:5000';

const app = createApp(App);
// 将 axios 挂载到全局，这样每个组件都可通过 this.$axios 调用（可选）
app.config.globalProperties.$axios = axios;

app.use(router);
app.mount('#app');
