import { AUTH_URL, saveToken } from "../api.js";

export default {
    template: `
        <main class="page-auth" :class="{ dark: store.dark }">
            <div class="auth-container">
                <div class="auth-card">
                    <h1 class="auth-title">{{ isLogin ? 'Login' : 'Register' }}</h1>
                    
                    <form @submit.prevent="submitAuth" class="auth-form">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input 
                                id="username"
                                v-model="username" 
                                type="text" 
                                placeholder="Enter your username"
                                class="form-input"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label for="password">Password</label>
                            <input 
                                id="password"
                                v-model="password" 
                                type="password" 
                                placeholder="Enter your password"
                                class="form-input"
                                required
                            />
                        </div>

                        <!-- Registration only: Confirm Password -->
                        <div v-if="!isLogin" class="form-group">
                            <label for="confirm-password">Confirm Password</label>
                            <input 
                                id="confirm-password"
                                v-model="confirmPassword" 
                                type="password" 
                                placeholder="Confirm your password"
                                class="form-input"
                                required
                            />
                        </div>

                        <!-- Captcha for both Login and Registration -->
                        <div class="form-group">
                            <label for="captcha">Captcha: {{ captchaQuestion }}</label>
                            <input 
                                id="captcha"
                                v-model="captchaAnswer" 
                                type="text" 
                                placeholder="Your answer"
                                class="form-input"
                                required
                            />
                        </div>

                        <!-- Error message -->
                        <div v-if="error" class="error-message">
                            {{ error }}
                        </div>

                        <!-- Loading state -->
                        <button 
                            type="submit" 
                            class="btn auth-btn"
                            :disabled="loading"
                        >
                            {{ loading ? 'Loading...' : (isLogin ? 'Login' : 'Register') }}
                        </button>
                    </form>

                    <!-- Toggle between login and register -->
                    <div class="auth-toggle">
                        <p>
                            {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
                            <button 
                                @click="isLogin = !isLogin"
                                class="toggle-btn"
                            >
                                {{ isLogin ? 'Register here' : 'Login here' }}
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </main>
    `,
    
    data() {
        return {
            isLogin: true,
            username: '',
            password: '',
            confirmPassword: '',
            captchaAnswer: '',
            error: '',
            loading: false,
            captchaNum1: 0,
            captchaNum2: 0,
            store: this.$root.$data.store
        };
    },

    computed: {
        captchaQuestion() {
            return `${this.captchaNum1} + ${this.captchaNum2} = ?`;
        },

        captchaCorrect() {
            return this.captchaNum1 + this.captchaNum2;
        }
    },

    watch: {
        isLogin() {
            this.error = '';
            this.password = '';
            this.confirmPassword = '';
            this.captchaAnswer = '';
            this.generateCaptcha();
        }
    },

    methods: {
        generateCaptcha() {
            this.captchaNum1 = Math.floor(Math.random() * 10) + 1;
            this.captchaNum2 = Math.floor(Math.random() * 10) + 1;
        },

        async submitAuth() {
            this.error = '';
            this.loading = true;

            try {
                // Validation
                if (!this.username || !this.password) {
                    this.error = 'Please fill all fields';
                    this.loading = false;
                    return;
                }

                // Captcha validation for both login and registration
                if (parseInt(this.captchaAnswer) !== this.captchaCorrect) {
                    this.error = 'Captcha answer is incorrect';
                    this.generateCaptcha();
                    this.captchaAnswer = '';
                    this.loading = false;
                    return;
                }

                if (!this.isLogin) {
                    if (this.password !== this.confirmPassword) {
                        this.error = 'Passwords do not match';
                        this.loading = false;
                        return;
                    }
                }

                // Send request to API
                const response = await fetch(`${AUTH_URL}/api/auth`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({
                        mode: this.isLogin ? 'login' : 'reg',
                        user: this.username,
                        pwd: this.password
                    })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Сохранить токен
                    if (data.token) {
                        saveToken(data.token);
                    }
                    
                    // Save to store
                    this.store.login(this.username, data.token);
                    
                    // Redirect to profile
                    this.$router.push('/profile');
                } else {
                    this.error = data.message || 'Authentication failed';
                }
            } catch (err) {
                this.error = 'Error: ' + err.message;
            } finally {
                this.loading = false;
            }
        }
    },

    mounted() {
        this.generateCaptcha();
    }
};
