import axios from 'axios'

export function getErrorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
        if (!error.response) return 'Cannot reach the server.'
        if (error.response.status === 429) return 'Too many requests. Please wait a moment.'

        const detail = error.response.data?.detail
        if (typeof detail === 'string') return detail
        if (Array.isArray(detail)) return detail.map((d) => d.msg).join('. ')
    }

    // Un error que no viene de la API es un fallo del front: se muestra en la consola
    if (import.meta.env.DEV) console.error(error)
    return 'Something went wrong.'
}