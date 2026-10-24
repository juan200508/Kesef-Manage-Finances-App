import axios from 'axios'

const TOKEN_KEY = 'kesef_token'

export const tokenStorage = {
    get: () => localStorage.getItem(TOKEN_KEY),
    set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
    clear: () => localStorage.removeItem(TOKEN_KEY)
}

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL})

// Antes de cada petición: agrega el token si existe
api.interceptors.request.use((config) => {
    const token = tokenStorage.get()
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
})

// Si el backend responde 401 con una sesión activa, el token venció: se cierra la sesión
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.responde?.status == 401 && tokenStorage.get()) {
            tokenStorage.clear()
            window.dispatchEvent(new Event('auth:logout'))
        }
        return Promise.reject(error)
    }
)