import { API_URL, clearToken } from "../api.js";

export default {
    template: `
        <main class="page-profile" :class="{ dark: store.dark }">
            <div class="profile-container" v-if="store.user">
                <div class="profile-card">
                    <div class="profile-header">
                        <h1 class="profile-username">{{ store.user }}</h1>
                        <button @click="logout" class="btn btn-danger">Logout</button>
                    </div>

                    <!-- Profile Stats -->
                    <div v-if="userProfile" class="profile-stats">
                        <div class="stat">
                            <span class="stat-label">Rank</span>
                            <span class="stat-value">#{{ userProfile.rank }}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Total Points</span>
                            <span class="stat-value">{{ userProfile.totalPoints }}</span>
                        </div>
                    </div>

                    <!-- Completed Levels -->
                    <div v-if="userProfile && userProfile.completedLevels.length > 0" class="profile-levels">
                        <h2>Completed Levels</h2>
                        <table class="levels-table">
                            <thead>
                                <tr>
                                    <th>Level</th>
                                    <th>Points</th>
                                    <th>YouTube</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="level in userProfile.completedLevels" :key="level.name">
                                    <td>{{ level.name }}</td>
                                    <td>{{ level.points }}</td>
                                    <td>
                                        <a 
                                            v-if="level.youtube" 
                                            :href="level.youtube" 
                                            target="_blank"
                                            class="btn btn-small"
                                        >
                                            Watch
                                        </a>
                                        <span v-else>—</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Not found in leaderboard -->
                    <div v-else-if="userProfile && userProfile.completedLevels.length === 0" class="no-levels">
                        <p>You haven't completed any levels yet.</p>
                    </div>

                    <!-- Loading -->
                    <div v-else class="loading">
                        <p>Loading profile...</p>
                    </div>
                </div>
            </div>

            <!-- Not logged in -->
            <div v-else class="not-logged-in">
                <h1>Please log in</h1>
                <router-link to="/auth" class="btn">Go to Login</router-link>
            </div>
        </main>
    `,

    data() {
        return {
            store: this.$root.$data.store,
            userProfile: null,
            error: ''
        };
    },

    methods: {
        async fetchProfile() {
            try {
                const response = await fetch(`${API_URL}/api/profile`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    this.userProfile = data.profile;
                } else {
                    this.error = 'Failed to load profile';
                }
            } catch (err) {
                this.error = 'Error: ' + err.message;
            }
        },

        logout() {
            clearToken();
            this.store.logout();
            this.$router.push('/auth');
        }
    },

    mounted() {
        if (this.store.user) {
            this.fetchProfile();
        }
    }
};
