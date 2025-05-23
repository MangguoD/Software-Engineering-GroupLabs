<template>
    <div>
      <h2>用户注册</h2>
      <form @submit.prevent="register">
        <div>
          <label>用户名: </label>
          <input v-model="username" type="text" required />
        </div>
        <div>
          <label>密码: </label>
          <input v-model="password" type="password" required />
        </div>
        <div>
          <label>姓名: </label>
          <input v-model="name" type="text" required />
        </div>
        <div>
          <label>角色: </label>
          <select v-model="role">
            <option value="student">学生</option>
            <option value="tutor">家教</option>
          </select>
        </div>
        <button type="submit">注册</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'Register',
    data() {
      return {
        username: '',
        password: '',
        name: '',
        role: 'student',
        message: ''
      };
    },
    methods: {
      async register() {
        this.message = '';
        try {
          const response = await axios.post('/register', {
            username: this.username,
            password: this.password,
            name: this.name,
            role: this.role
          });
          if (response.data.success) {
            this.message = '注册成功！正在跳转到登录...';
            // 短暂延迟后跳转到登录页
            setTimeout(() => {
              this.$router.push('/login');
            }, 1000);
          } else {
            this.message = response.data.message || '注册失败';
          }
        } catch (error) {
          this.message = error.response?.data?.message || '注册时发生错误';
        }
      }
    }
  };
  </script>
  <style scoped>
h2 {
    color: var(--primary-color);
    text-align: center;
    margin-bottom: 2rem;
}

form {
    max-width: 400px;
}
</style>  