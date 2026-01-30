import routes from './routes.js';
import { store } from './store.js';

console.log('Vue version:', Vue.version);
console.log('Vue Router version:', VueRouter.version);

const app = Vue.createApp({
    data: () => ({ store }),
    watch: {
        'store.dark'(newVal) {
            // Update HTML class when dark mode changes
            document.documentElement.classList.toggle('dark', newVal);
        }
    },
    mounted() {
        // Set initial HTML class based on store
        document.documentElement.classList.toggle('dark', this.store.dark);
    }
});
const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes,
});

console.log('App created, mounting router...');
app.use(router);

console.log('About to mount app');
app.mount('#app');
console.log('App mounted successfully');
