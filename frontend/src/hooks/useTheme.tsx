import { useState } from 'react'

export type Theme = 'light' | 'dark'
const STORAGE_KEY = 'kesef_theme'

export function useTheme() {
    const [theme, setTheme] = useState<Theme>(() =>
        document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'
    )

    const toggleTheme = () => {
        const next: Theme = theme === 'dark' ? 'light' : 'dark'
        document.documentElement.dataset.theme = next
        try {
            localStorage.setItem(STORAGE_KEY, next)
        } catch {
            // modo privado o storage bloqueado: el tema solo dura la sesión
        }
        setTheme(next)
    }

    return { theme, toggleTheme }
}