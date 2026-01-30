import List from './pages/List.js';
import Leaderboard from './pages/Leaderboard.js';
import Roulette from './pages/Roulette.js';
import Auth from './pages/Auth.js';
import Profile from './pages/Profile.js';

export default [
    { path: '/', component: List },
    { path: '/leaderboard', component: Leaderboard },
    { path: '/roulette', component: Roulette },
    { path: '/auth', component: Auth },
    { path: '/profile', component: Profile },
];
