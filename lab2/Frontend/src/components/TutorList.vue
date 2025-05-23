<template>
    <div>
      <h2>{{ mode === 'recommended' ? '推荐的家教列表' : '家教列表' }}</h2>
      <div v-if="mode === 'all'">
        <input v-model="filterSubject" placeholder="按科目搜索" />
        <button @click="search">搜索</button>
      </div>
      <ul>
        <li v-for="tutor in tutors" :key="tutor.id">
          {{ tutor.name }} - 科目: {{ tutor.subjects }} - 城市: {{ tutor.city }}
          <router-link :to="`/tutor/${tutor.user_id}`">查看详情</router-link>
        </li>
      </ul>
      <p v-if="tutors.length === 0">暂无家教信息</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'TutorList',
    props: {
      mode: {
        type: String,
        default: 'all'
      }
    },
    data() {
      return {
        tutors: [],
        filterSubject: ''
      };
    },
    async created() {
      if (this.mode === 'recommended') {
        // 获取当前用户并调用推荐接口
        const userStr = window.localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          if (user && user.role === 'student') {
            const res = await axios.get(`/recommend/student/${user.id}`);
            if (res.data && res.data.success) {
              this.tutors = res.data.recommended_tutors;
            }
          }
        }
      } else {
        // 获取全部家教列表
        const res = await axios.get('/tutors');
        if (res.data && res.data.success) {
          this.tutors = res.data.tutors;
        }
      }
    },
    methods: {
      async search() {
        let url = '/tutors';
        if (this.filterSubject) {
          url += '?subject=' + encodeURIComponent(this.filterSubject);
        }
        const res = await axios.get(url);
        if (res.data && res.data.success) {
          this.tutors = res.data.tutors;
        }
      }
    }
  };
  </script>
  <style scoped>
ul {
    display: grid;
    gap: 1rem;
}

li {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: bold;
}

a:hover {
    text-decoration: underline;
}
</style>