import { createContext, useContext } from 'react'

type AuthContextValue = {
    isAuthenticated: boolean
    sessionExpired: boolean
    signIn: (token: string) => void
    signOut: () => void
}
export const AuthContext = createContext<AuthContextValue | null>(null) 

export function useAuth() {
    const ctx = useContext(AuthContext)
    if (!ctx) throw new Error('useAuth must be user inside <AuthProvider>')
    return ctx
}
