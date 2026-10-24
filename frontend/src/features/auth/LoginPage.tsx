import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import { Link, Navigate } from 'react-router-dom'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Input } from '../../components/ui/Input'
import { getErrorMessage } from '../../api/errors'
import type { LoginInput } from '../../api/types'
import { login } from './api'
import { useAuth } from './auth-context'

export function LoginPage() {
    const { isAuthenticated, signIn } = useAuth()
    const { register, handleSubmit, formState: { errors } } = useForm<LoginInput>()

    const mutation = useMutation({
        mutationFn: login,
        onSuccess: (data) => signIn(data.access_token),
    })

    if (isAuthenticated) return <Navigate to="/" replace />

    return (
        <main className="mx-auto mt-24 max-w-sm px-4">
        <Card className="space-y-4">
            <h1 className="text-xl font-semibold">Sign in</h1>

            <form onSubmit={handleSubmit((values) => mutation.mutate(values))} className="space-y-3">
            <div className="space-y-1">
                <Input type="email" placeholder="Email" {...register('email', { required: 'Email is required' })} />
                {errors.email && <p className="text-xs text-expense">{errors.email.message}</p>}
            </div>

            <div className="space-y-1">
                <Input type="password" placeholder="Password" {...register('password', { required: 'Password is required' })} />
                {errors.password && <p className="text-xs text-expense">{errors.password.message}</p>}
            </div>

            {mutation.isError && (
                <p className="text-sm text-expense">{getErrorMessage(mutation.error)}</p>
            )}

            <Button type="submit" className="w-full justify-center" disabled={mutation.isPending}>
                {mutation.isPending ? 'Signing in…' : 'Sign in'}
            </Button>
            </form>

            <p className="text-sm text-content-muted">
            No account? <Link to="/register" className="text-brand">Create one</Link>
            </p>
        </Card>
        </main>
    )
}