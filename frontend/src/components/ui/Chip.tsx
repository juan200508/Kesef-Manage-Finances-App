import type { ComponentProps } from 'react'

interface Props extends ComponentProps<'button'> {
    active: boolean
}

export function Chip({ active, className = '', ...props }: Props) {
    return (
        <button
            type="button"
            className={
                'cursor-pointer rounded-lg px-3 py-1.5 text-sm transition-colors ' +
                (active
                    ? 'bg-brand text-on-brand'
                    : 'border border-line text-content-muted hover:text-content') +
                ` ${className}`
            }
            {...props}
        />
    )
}