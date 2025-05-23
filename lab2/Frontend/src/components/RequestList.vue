<template>
    <div>
      <h2>{{ mode === 'recommended' ? '推荐的学生需求列表' : '学生需求列表' }}</h2>
      <div v-if="mode === 'all'">
        <input v-model="filterSubject" placeholder="按科目搜索" />
        <button @click="search">搜索</button>
      </div>
      <ul>
        <li v-for="req in requests" :key="req.id">
          {{ req.name }} - 科目: {{ req.subject }} - 城市: {{ req.city }} - {{ req.description }}
        </li>
      </ul>
      <p v-if="requests.length === 0">暂无学生需求信息</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'RequestList',
    props: {
      mode: {
        type: String,
        default: 'all'
      }
    },
    data() {
      return {
        requests: [],
        filterSubject: ''
      };
    },
    async created() {
      if (this.mode === 'recommended') {
        const userStr = window.localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          if (user && user.role === 'tutor') {
            const res = await axios.get(`/recommend/tutor/${user.id}`);
            if (res.data && res.data.success) {
              this.requests = res.data.recommended_requests;
            }
          }
        }
      } else {
        const res = await axios.get('/requests');
        if (res.data && res.data.success) {
          this.requests = res.data.requests;
        }
      }
    },
    methods: {
      async search() {
        let url = '/requests';
        if (this.filterSubject) {
          url += '?subject=' + encodeURIComponent(this.filterSubject);
        }
        const res = await axios.get(url);
        if (res.data && res.data.success) {
          this.requests = res.data.requests;
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