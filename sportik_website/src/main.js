import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@fortawesome/fontawesome-free/css/all.css';
import '@/rgblind/rgblind/rgblind.css';

const hostname= "http://127.0.0.1:5000";

const app = createApp(App);
app.use(router).provide("$hostname", hostname);


app.mount('#app');
