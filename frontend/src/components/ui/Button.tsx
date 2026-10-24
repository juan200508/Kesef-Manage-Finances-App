import type { ButtonHTMLAttributes } from 'react'

type Variant = 'primary' | 'ghost' | 'danger'
type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }

const variants: Record<Variant, string> = {
    primary: 'bg-brand text-on-brand hover:bg-brand-hover',
    ghost: 'bg-transparent text-content hover:bg-surface-muted',
    danger: 'bg-expense text-on-brand hover:opacity-90',
}

export function Button({ variant = 'primary', className = '', ...props }: ButtonProps) {
    return (
        <button
            className={`inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition-colors disabled:opacity-50 ${variants[variant]} ${className}`}
            {...props}
        />
    )
}