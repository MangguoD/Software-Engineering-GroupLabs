<template>
    <div>
      <h2>问答系统</h2>
      <div>
        <input v-model="question" @keyup.enter="ask" placeholder="请输入您的问题" />
        <button @click="ask">提问</button>
      </div>
      <div v-for="(msg, index) in messages" :key="index" class="qa-pair">
        <p><strong>问:</strong> {{ msg.q }}</p>
        <p><strong>答:</strong> {{ msg.a }}</p>
        <hr />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'QA',
    data() {
      return {
        question: '',
        messages: []
      };
    },
    methods: {
      async ask() {
        if (!this.question.trim()) {
          return;
        }
        const q = this.question.trim();
        try {
          const res = await axios.get('/qa', {
            params: { question: q }
          });
          if (res.data) {
            this.messages.push({ q: q, a: res.data.answer });
          }
        } catch (error) {
          this.messages.push({ q: q, a: '（无法获取回答）' });
        }
        this.question = '';
      }
    }
  };
  </script>
  
<style scoped>
.qa-pair {
    background: white;
    padding: 1.5rem;
    border-left: 4px solid var(--primary-color);
    margin-bottom: 1.5rem;
}

input {
    width: 70%;
    margin-right: 10px;
}
</style>