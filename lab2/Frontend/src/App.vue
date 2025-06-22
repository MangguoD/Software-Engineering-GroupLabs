<template>
    <div>
      <!-- 导航栏 -->
      <nav>
        <ul>
          <!-- 未登录时显示 注册/登录 链接 -->
          <li v-if="!currentUser"><router-link to="/login">登录</router-link></li>
          <li v-if="!currentUser"><router-link to="/register">注册</router-link></li>
          <!-- 学生用户登录后看到的菜单 -->
          <li v-if="currentUser && currentUser.role === 'student'"><router-link to="/recommend-tutors">推荐家教</router-link></li>
          <li v-if="currentUser && currentUser.role === 'student'"><router-link to="/tutors">查找家教</router-link></li>
          <li v-if="currentUser && currentUser.role === 'student'"><router-link to="/new-request">发布需求</router-link></li>
          <!-- 家教用户登录后看到的菜单 -->
          <li v-if="currentUser && currentUser.role === 'tutor'"><router-link to="/recommend-students">推荐学生</router-link></li>
          <li v-if="currentUser && currentUser.role === 'tutor'"><router-link to="/requests">查找学生</router-link></li>
          <li v-if="currentUser && currentUser.role === 'tutor'"><router-link to="/new-profile">发布家教信息</router-link></li>
          <!-- 公共菜单 -->
          <li v-if="currentUser"><router-link to="/qa">问答</router-link></li>
          <li v-if="currentUser"><a href="#" @click.prevent="logout">注销 ({{ currentUser.name }})</a></li>
        </ul>
      </nav>
      <!-- 路由出口 -->
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: 'App',
    data() {
      return {
        currentUser: null  // 当前登录用户信息
      };
    },
    created() {
      // 尝试从localStorage载入用户信息
      const userStr = window.localStorage.getItem('user');
      if (userStr) {
        try {
          this.currentUser = JSON.parse(userStr);
        } catch (e) {
          this.currentUser = null;
        }
      }
    },
    methods: {
      logout() {
        // 注销：清除存储并跳转到登录页
        window.localStorage.removeItem('user');
        this.currentUser = null;
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style>
  :root {
    --primary-color: rgb(43, 59, 41);
    --bg-color: #f2f2f2;
    --text-primary: rgb(18, 46, 14);
    --text-secondary: rgb(183, 211, 180);
    --hover-bg: rgb(60, 72, 59);
}

/* 添加全局基础样式 */
body {
    background-color: var(--bg-color);
    color: var(--text-primary);
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
}

nav {
    background-color: var(--primary-color);
    padding: 1rem;
    margin-bottom: 2rem;
    border-radius: 8px;
}

nav ul li a {
    color: white !important;
    background-color: var(--primary-color);
    text-decoration: none;
    padding: 16px 32px;
    border-radius: 4px;
    transition: background-color 0.3s;
}

nav ul li a:hover {
    background-color: var(--hover-bg);
}

/* 通用表单样式 */
form {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 20px auto;
}

input, textarea, select {
    width: 100%;
    padding: 8px;
    margin: 8px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

button {
    background-color: var(--primary-color);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: var(--hover-bg);
}

/* 列表样式 */
ul {
    background: var(--bg-color);
    list-style: none;
    padding: 0;
}

ul li {
    background: var(--bg-color);
    color: var(--text-primary);
    /* padding: 1rem; */
    margin-bottom: 1rem;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

ul li a {
    /* font-size: 1.2rem; */
    color: var(--text-primary) !important; 
    text-decoration: none;
    /* font-weight: bold; */
}

/* 消息提示 */
p[v-if^="message"] {
    color: var(--text-secondary);
    padding: 10px;
    border-radius: 4px;
    margin-top: 1rem;
}
nav ul {
  background-color: var(--primary-color) !important;
  list-style: none;
  padding: 0;
}
nav ul li {
  display: inline-block;
  margin-right: 15px;
}
</style>