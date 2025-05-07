<template>
    <div>
      <h2>发布家教信息</h2>
      <form @submit.prevent="submitProfile">
        <div>
          <label>教授科目: </label>
          <input v-model="subjects" type="text" placeholder="例: 数学, 英语" required />
        </div>
        <div>
          <label>所在城市: </label>
          <input v-model="city" type="text" placeholder="例: 北京" required />
        </div>
        <div>
          <label>简介: </label>
          <textarea v-model="description" placeholder="填写您的教学经验或特长"></textarea>
        </div>
        <button type="submit">提交</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'TutorProfileForm',
    data() {
      return {
        subjects: '',
        city: '',
        description: '',
        message: ''
      };
    },
    methods: {
      async submitProfile() {
        this.message = '';
        const userStr = window.localStorage.getItem('user');
        if (!userStr) {
          this.message = '请先登录';
          return;
        }
        const user = JSON.parse(userStr);
        if (user.role !== 'tutor') {
          this.message = '只有家教用户可以发布家教信息';
          return;
        }
        try {
          const res = await axios.post('/tutor/profile', {
            user_id: user.id,
            subjects: this.subjects,
            city: this.city,
            description: this.description
          });
          if (res.data && res.data.success) {
            this.message = '发布成功！';
            // 跳转到自己发布的家教详情页
            this.$router.push(`/tutor/${user.id}`);
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
  