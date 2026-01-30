// Shared reactive store — extracted to avoid circular imports
export const store = Vue.reactive({
    dark: JSON.parse(localStorage.getItem('dark')) || false,
    user: localStorage.getItem('auth_user') || null,
    token: localStorage.getItem('auth_token') || null,
    
    toggleDark() {
        this.dark = !this.dark;
        localStorage.setItem('dark', JSON.stringify(this.dark));
    },

    login(username, token) {
        this.user = username;
        this.token = token;
        localStorage.setItem('auth_user', username);
        if (token) {
            localStorage.setItem('auth_token', token);
        }
    },

    logout() {
        this.user = null;
        this.token = null;
        localStorage.removeItem('auth_user');
        localStorage.removeItem('auth_token');
    },
});
