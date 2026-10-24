import type { ComponentProps } from 'react'

export function Select({ className = '', ...props }: ComponentProps<'select'>) {
    return (
        <select
            className={`w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm outline-none focus:border-brand ${className}`}
            {...props}
        />
    )
}