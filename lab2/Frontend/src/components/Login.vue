<template>
    <div>
      <h2>用户登录</h2>
      <form @submit.prevent="login">
        <div>
          <label>用户名: </label>
          <input v-model="username" type="text" required />
        </div>
        <div>
          <label>密码: </label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit">登录</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'Login',
    data() {
      return {
        username: '',
        password: '',
        message: ''
      };
    },
    methods: {
      async login() {
        this.message = '';
        try {
          const response = await axios.post('/login', {
            username: this.username,
            password: this.password
          });
          if (response.data.success) {
            // 登录成功，保存用户信息
            window.localStorage.setItem('user', JSON.stringify(response.data.user));
            this.message = '登录成功！';
            // 根据角色跳转到相应主页
            const userRole = response.data.user.role;
            if (userRole === 'student') {
              window.location.href = '/recommend-tutors';
            } else if (userRole === 'tutor') {
              window.location.href = '/recommend-students';
            } else {
              window.location.href = '/tutors';
            }
          } else {
            this.message = response.data.message || '登录失败';
          }
        } catch (error) {
          this.message = error.response?.data?.message || '登录时发生错误';
        }
      }
    }
  };
  </script>
  