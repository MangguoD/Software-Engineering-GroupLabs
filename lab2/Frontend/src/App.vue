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
  nav ul {
    list-style: none;
    padding: 0;
  }
  nav ul li {
    display: inline-block;
    margin-right: 15px;
  }
  </style>
  