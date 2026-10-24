import type { ComponentProps } from 'react'

export function Input({ className = '', ...props }: ComponentProps<'input'>) {
    return (
        <input
        className={`w-full rounded-md border border-line bg-surface px-3 py-1.5 text-sm text-content placeholder:text-content-muted focus:border-brand focus:outline-none ${className}`}
        {...props}
        />
    )
}