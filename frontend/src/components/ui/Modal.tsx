import type { ReactNode } from 'react'
import { Card } from './Card'

interface Props {
    title: string
    onClose: () => void
    children: ReactNode,
    className?: string
}

export function Modal({ title, onClose, children, className= 'max-w-md' }: Props) {
    return (
        <div
            className="fixed inset-0 z-40 flex items-center justify-center bg-black/50 p-4"
            onClick={onClose}
        >
            {/* stopPropagation: un clic dentro de la tarjeta no debe cerrar el modal */}
            <div className={`w-full ${className}`}  onClick={(e) => e.stopPropagation()}>
                <Card className="space-y-4">
                    <h2 className="text-lg font-semibold">{title}</h2>
                    {children}
                </Card>
            </div>
        </div>
    )
}