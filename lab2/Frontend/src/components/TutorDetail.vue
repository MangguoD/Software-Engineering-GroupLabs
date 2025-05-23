<template>
    <div v-if="tutor">
      <h2>家教详情</h2>
      <p><strong>姓名:</strong> {{ tutor.name }}</p>
      <p><strong>科目:</strong> {{ tutor.subjects }}</p>
      <p><strong>城市:</strong> {{ tutor.city }}</p>
      <p><strong>简介:</strong> {{ tutor.description }}</p>
      <p v-if="tutor.average_rating !== null"><strong>平均评分:</strong> {{ tutor.average_rating }}</p>
      <h3>学生评价</h3>
      <ul>
        <li v-for="(review, index) in tutor.reviews" :key="index">
          评分: {{ review.rating }} - 评论: "{{ review.comment }}" 
          <span>- 学生: {{ review.student_name }}</span>
        </li>
      </ul>
      <p v-if="tutor.reviews.length === 0">暂时没有评价</p>
      <!-- 只有学生用户可以评价 -->
      <div v-if="canReview">
        <h4>添加评价:</h4>
        <form @submit.prevent="submitReview">
          <div>
            <label>评分: </label>
            <select v-model.number="newRating">
              <option disabled value="">请选择评分</option>
              <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>
          </div>
          <div>
            <label>评论: </label>
            <textarea v-model="newComment" placeholder="写下您的评价"></textarea>
          </div>
          <button type="submit">提交评价</button>
        </form>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
    <p v-else>加载中...</p>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'TutorDetail',
    props: ['id'],
    data() {
      return {
        tutor: null,
        newRating: '',
        newComment: '',
        message: ''
      };
    },
    computed: {
      // 当前用户是否可以评价（登录且为学生）
      canReview() {
        const userStr = window.localStorage.getItem('user');
        if (!userStr) return false;
        const user = JSON.parse(userStr);
        return user.role === 'student';
      }
    },
    async created() {
      const res = await axios.get(`/tutor/${this.id}`);
      if (res.data && res.data.success) {
        this.tutor = res.data.tutor;
        if (!this.tutor.reviews) {
          this.tutor.reviews = [];
        }
        if (this.tutor.average_rating === null) {
          this.tutor.average_rating = null;
        }
      } else {
        this.message = res.data.message || '加载失败';
      }
    },
    methods: {
      async submitReview() {
        this.message = '';
        const userStr = window.localStorage.getItem('user');
        if (!userStr) {
          this.message = '请先登录';
          return;
        }
        const user = JSON.parse(userStr);
        if (user.role !== 'student') {
          this.message = '只有学生用户可以评价';
          return;
        }
        if (!this.newRating) {
          this.message = '请选择评分';
          return;
        }
        try {
          const res = await axios.post('/review', {
            tutor_id: this.tutor.id,
            student_id: user.id,
            rating: this.newRating,
            comment: this.newComment
          });
          if (res.data && res.data.success) {
            this.message = '评价提交成功！';
            // 将新评价添加到列表并更新平均分
            this.tutor.reviews.push({
              rating: this.newRating,
              comment: this.newComment || '',
              student_name: user.name
            });
            const total = this.tutor.reviews.reduce((sum, r) => sum + (r.rating || 0), 0);
            this.tutor.average_rating = (total / this.tutor.reviews.length).toFixed(1);
            // 重置表单
            this.newRating = '';
            this.newComment = '';
          } else {
            this.message = res.data.message || '提交失败';
          }
        } catch (error) {
          this.message = error.response?.data?.message || '提交评价时发生错误';
        }
      }
    }
  };
  </script>
  <style scoped>
div {
    background: white;
    padding: 2rem;
    border-radius: 8px;
}

h3 {
    color: var(--text-secondary);
    border-bottom: 2px solid var(--bg-color);
    padding-bottom: 0.5rem;
}
</style>