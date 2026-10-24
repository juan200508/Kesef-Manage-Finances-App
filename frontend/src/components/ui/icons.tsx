import type { ReactNode } from 'react'

interface IconProps {
    size?: number
}

function Svg({ size = 16, children }: IconProps & { children: ReactNode }) {
    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth={1.8}
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            {children}
        </svg>
    )
}

export const MenuIcon = ({ size = 20 }: IconProps) => (
    <Svg size={size}>
        <path d="M3 6h18M3 12h18M3 18h18" />
    </Svg>
)

export const RepeatIcon = ({ size }: IconProps) => (
    <Svg size={size}>
        <polyline points="17 1 21 5 17 9" />
        <path d="M3 11V9a4 4 0 0 1 4-4h14" />
        <polyline points="7 23 3 19 7 15" />
        <path d="M21 13v2a4 4 0 0 1-4 4H3" />
    </Svg>
)

export const TrendingUpIcon = ({ size }: IconProps) => (
    <Svg size={size}>
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
        <polyline points="17 6 23 6 23 12" />
    </Svg>
)

export const TagIcon = ({ size }: IconProps) => (
    <Svg size={size}>
        <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" />
        <line x1="7" y1="7" x2="7.01" y2="7" />
    </Svg>
)

export const CloseIcon = ({ size = 20 }: IconProps) => (
    <Svg size={size}>
        <path d="M18 6 6 18M6 6l12 12" />
    </Svg>
)