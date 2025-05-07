<template>
    <div>
      <h2>发布学生需求</h2>
      <form @submit.prevent="submitRequest">
        <div>
          <label>需要辅导科目: </label>
          <input v-model="subject" type="text" required />
        </div>
        <div>
          <label>所在城市: </label>
          <input v-model="city" type="text" required />
        </div>
        <div>
          <label>需求描述: </label>
          <textarea v-model="description" placeholder="描述具体需求（可选）"></textarea>
        </div>
        <button type="submit">提交</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'StudentRequestForm',
    data() {
      return {
        subject: '',
        city: '',
        description: '',
        message: ''
      };
    },
    methods: {
      async submitRequest() {
        this.message = '';
        const userStr = window.localStorage.getItem('user');
        if (!userStr) {
          this.message = '请先登录';
          return;
        }
        const user = JSON.parse(userStr);
        if (user.role !== 'student') {
          this.message = '只有学生用户可以发布需求';
          return;
        }
        try {
          const res = await axios.post('/student/request', {
            user_id: user.id,
            subject: this.subject,
            city: this.city,
            description: this.description
          });
          if (res.data && res.data.success) {
            this.message = '发布成功！正在查找推荐家教...';
            // 跳转到推荐家教页面
            this.$router.push('/recommend-tutors');
          } else {
            this.message = res.data.message || '提交失败';
          }
        } catch (error) {
          this.message = error.response?.data?.message || '提交时发生错误';
        }
      }
    }
  };
  </script>
  