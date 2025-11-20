// API Client для работы с Django бэкендом (Django сессии)
const API_BASE_URL = '/api';

class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.csrfToken = null;
        this.getCSRFToken();
    }

    async getCSRFToken() {
        try {
            // Получаем CSRF токен из cookies
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    this.csrfToken = decodeURIComponent(value);
                    return;
                }
            }
            // Если токена нет в cookies, пробуем из window
            if (window.csrftoken) {
                this.csrfToken = window.csrftoken;
                return;
            }
            // Если токена нет, получаем через API
            const response = await fetch('/api/csrf-token/', {
                method: 'GET',
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                this.csrfToken = data.csrftoken;
            }
        } catch (error) {
            console.error('Ошибка получения CSRF токена:', error);
        }
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            credentials: 'include',  // Важно для работы с Django сессиями
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        // Добавляем CSRF токен для POST/PUT/DELETE запросов
        if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(options.method || 'GET')) {
            if (this.csrfToken) {
                config.headers['X-CSRFToken'] = this.csrfToken;
            }
        }

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            
            // Если 403, пробуем обновить CSRF токен
            if (response.status === 403) {
                await this.getCSRFToken();
                if (this.csrfToken && ['POST', 'PUT', 'DELETE', 'PATCH'].includes(options.method || 'GET')) {
                    config.headers['X-CSRFToken'] = this.csrfToken;
                    const retryResponse = await fetch(url, config);
                    if (retryResponse.ok) {
                        return await retryResponse.json();
                    }
                }
            }
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || (data.errors && JSON.stringify(data.errors)) || 'Ошибка запроса');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async register(username, email, password, confirmPassword) {
        return this.request('/register/', {
            method: 'POST',
            body: { username, email, password, confirm_password: confirmPassword }
        });
    }

    async login(email, password, rememberMe = false) {
        return this.request('/login/', {
            method: 'POST',
            body: { email, password, remember_me: rememberMe }
        });
    }

    async logout() {
        return this.request('/logout/', {
            method: 'POST'
        });
    }

    async validateSession() {
        return this.request('/validate-session/', {
            method: 'GET'
        });
    }

    async getProfile() {
        return this.request('/profile/', {
            method: 'GET'
        });
    }

    async updateSettings(settings) {
        return this.request('/settings/', {
            method: 'PUT',
            body: settings
        });
    }

    async changePassword(currentPassword, newPassword, confirmPassword) {
        return this.request('/change-password/', {
            method: 'POST',
            body: {
                current_password: currentPassword,
                new_password: newPassword,
                confirm_password: confirmPassword
            }
        });
    }

    async changeUsername(newUsername) {
        return this.request('/change-username/', {
            method: 'POST',
            body: {
                new_username: newUsername
            }
        });
    }

    async deleteAccount() {
        return this.request('/delete-account/', {
            method: 'POST'
        });
    }

    async getGames() {
        return this.request('/games/', {
            method: 'GET'
        });
    }

    async startGameSession(gameType) {
        return this.request('/start-game/', {
            method: 'POST',
            body: {
                game_type: gameType
            }
        });
    }
}

// Создаем глобальный экземпляр API клиента
const apiClient = new APIClient();

