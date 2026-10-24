import type { ReactNode } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '../features/auth/AuthProvider'

const queryClient = new QueryClient({
    defaultOptions: {
        // Sin reintentos automáticos: un 401, un 404 o un 429 no se arreglan repitiendo,
        // y cada reintento gastaría tu cupo de rate limiting.
        queries: { retry: false, refetchOnWindowFocus: false },
    },
})

export function Providers({ children }: { children: ReactNode }) {
    return (
        <QueryClientProvider client={queryClient}>
        <AuthProvider>{children}</AuthProvider>
        </QueryClientProvider>
    )
}