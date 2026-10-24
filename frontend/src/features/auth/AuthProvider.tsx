import { useEffect, useState, type ReactNode } from 'react'
import { tokenStorage } from '../../api/client'
import { AuthContext } from './auth-context'

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(() => tokenStorage.get())

    const signIn = (newToken: string) => {
        tokenStorage.set(newToken)
        setToken(newToken)
    }

    const signOut = () => {
        tokenStorage.clear()
        setToken(null)
    }

    // El cliente de API avisa con este evento cuando el token venció (401)
    useEffect(() => {
        const onLogout = () => setToken(null)
        window.addEventListener('auth:logout', onLogout)
        return () => window.removeEventListener('auth:logout', onLogout)
    }, [])

    return (
        <AuthContext value={{ isAuthenticated: token !== null, signIn, signOut }}>
        {children}
        </AuthContext>
    )
}