import { useState, type ReactNode } from 'react'
import { ToastContext, type ToastKind } from './toast-context'

interface ToastItem {
    id: number
    kind: ToastKind
    message: string
}

const DURATION_MS = 4000
let nextId = 0

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toasts, setToasts] = useState<ToastItem[]>([])

    const dismiss = (id: number) => setToasts((prev) => prev.filter((t) => t.id !== id))

    const push = (kind: ToastKind, message: string) => {
        const id = nextId++
        setToasts((prev) => [...prev, { id, kind, message }])
        setTimeout(() => dismiss(id), DURATION_MS)
    }

    return (
        <ToastContext value={{ success: (m) => push('success', m), error: (m) => push('error', m) }}>
            {children}

            {/* z-[60]: por encima de los modales (z-40 y z-50) */}
            <div className="fixed right-4 bottom-4 z-60 flex w-80 max-w-[calc(100vw-2rem)] flex-col gap-2">
                {toasts.map((t) => (
                    <div
                        key={t.id}
                        className={
                            'toast-enter flex items-start justify-between gap-3 rounded-lg border border-line border-l-4 bg-surface px-4 py-3 text-sm shadow-lg ' +
                            (t.kind === 'success' ? 'border-l-income' : 'border-l-expense')
                        }
                    >
                        <span>{t.message}</span>
                        <button
                            type="button"
                            onClick={() => dismiss(t.id)}
                            className="cursor-pointer text-content-muted hover:text-content"
                        >
                            ✕
                        </button>
                    </div>
                ))}
            </div>
        </ToastContext>
    )
}