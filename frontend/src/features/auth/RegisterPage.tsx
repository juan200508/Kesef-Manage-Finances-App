import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import { Link, Navigate } from 'react-router-dom'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Input } from '../../components/ui/Input'
import { getErrorMessage } from '../../api/errors'
import type { RegisterInput } from '../../api/types'
import { login, register as registerUser } from './api'
import { useAuth } from './auth-context'

type RegisterForm = RegisterInput & {confirmPassword: string}

export function RegisterPage() {
    const { isAuthenticated, signIn } = useAuth()
    const { register, handleSubmit, getValues, formState: { errors } } = useForm<RegisterForm>()

    const mutation = useMutation({
        mutationFn: async (data: RegisterInput) => {
            await registerUser(data)
            return login({email: data.email, password: data.password})
        },
        onSuccess: (token) => signIn(token.access_token)
    })

    if (isAuthenticated) return <Navigate to="/" replace />

    return (
        <main className="mx-auto mt-24 max-w-sm px-4">

            <Card className="space-y-4">
                <h1 className="text-xl font-semibold">Sign up</h1>

                <form 
                    onSubmit={handleSubmit(({email, password, full_name}) => 
                        mutation.mutate({email, password, full_name: full_name || undefined})
                    )} 
                    className="space-y-3"
                >

                {/* Fullname */}
                <div className="space-y-1">
                    <Input type="text" placeholder="Full name (optional)" {...register('full_name')} />
                </div>

                {/* Email */}
                <div className="space-y-1">
                    <Input type="email" placeholder="Email" {...register('email', { required: 'Email is required' })} />
                    {errors.email && <p className="text-xs text-expense">{errors.email.message}</p>}
                </div>

                {/* Password */}
                <div className="space-y-1">
                    <Input type="password" placeholder="Password" 
                        {...register('password', 
                            {   required: 'Password is required', 
                                minLength: {value: 8, message: 'At least 8 characters'},
                                maxLength: {value: 72, message: 'At least 72 characters'},
                                deps: ['confirmPassword']
                            })} />
                    {errors.password && <p className="text-xs text-expense">{errors.password.message}</p>}
                </div>

                <div className="space-y-1">
                    <Input type='password' placeholder='Confirm your password'
                        {...register('confirmPassword', {
                            required: 'Please confirm your password',
                            validate: (value) => value === getValues('password') || 'Passwords do not match.'
                        })}
                    />
                    {errors.confirmPassword && <p className='text-xs text-expense'>{errors.confirmPassword.message}</p>}
                </div>
                

                {mutation.isError && (
                    <p className="text-sm text-expense">{getErrorMessage(mutation.error)}</p>
                )}

                <Button type="submit" className="w-full justify-center" disabled={mutation.isPending}>
                    {mutation.isPending ? 'Creating account…' : 'Create account'}
                </Button>
                </form>

                <p className="text-sm text-content-muted">
                Already have an account? <Link to="/login" className="text-brand">Sign in</Link>
                </p>
            </Card>
        </main>
    )
}