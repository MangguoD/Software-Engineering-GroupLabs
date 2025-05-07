// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Register from '../components/Register.vue';
import Login from '../components/Login.vue';
import TutorList from '../components/TutorList.vue';
import RequestList from '../components/RequestList.vue';
import TutorDetail from '../components/TutorDetail.vue';
import TutorProfileForm from '../components/TutorProfileForm.vue';
import StudentRequestForm from '../components/StudentRequestForm.vue';
import QA from '../components/QA.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/tutors', component: TutorList, props: { mode: 'all' } },
  { path: '/requests', component: RequestList, props: { mode: 'all' } },
  { path: '/recommend-tutors', component: TutorList, props: { mode: 'recommended' } },
  { path: '/recommend-students', component: RequestList, props: { mode: 'recommended' } },
  { path: '/tutor/:id', component: TutorDetail, props: true },
  { path: '/new-profile', component: TutorProfileForm },
  { path: '/new-request', component: StudentRequestForm },
  { path: '/qa', component: QA }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
