import { useEffect, useState, type ReactNode } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { tokenStorage } from '../../api/client'
import { AuthContext } from './auth-context'

export function AuthProvider({ children }: { children: ReactNode }) {
    const queryClient = useQueryClient()
    const [token, setToken] = useState<string | null>(() => tokenStorage.get())
    const [sessionExpired, setSessionExpired] = useState(false)

    const signIn = (newToken: string) => {
        tokenStorage.set(newToken)
        setToken(newToken)
        setSessionExpired(false)
    }

    const signOut = () => {
        tokenStorage.clear()
        setToken(null)
        queryClient.clear() // los datos de este usuario no deben verse en la siguiente sesión
    }

    // El cliente de API avisa con este evento cuando el token venció (401)
    useEffect(() => {
        const onLogout = () => {
            setToken(null)
            setSessionExpired(true)
            queryClient.clear()
        }
        window.addEventListener('auth:logout', onLogout)
        return () => window.removeEventListener('auth:logout', onLogout)
    }, [queryClient])

    return (
        <AuthContext value={{ isAuthenticated: token !== null, sessionExpired, signIn, signOut }}>
            {children}
        </AuthContext>
    )
}