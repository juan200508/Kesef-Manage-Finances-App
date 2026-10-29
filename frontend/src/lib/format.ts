import type { MovementType } from '../api/types'
import type { IncomeSource } from '../api/types'

const cop = new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
})

export const formatCurrency = (value: string | number) => cop.format(Number(value))

export const MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

export const MOVEMENT_TYPE_LABELS: Record<MovementType, string> = {
    COMPRA: 'Purchase',
    TRANSFERENCIA: 'Transfer',
    RETIRO: 'Withdrawal',
    PAGO: 'Payment',
    OTRO: 'Other',
}

export const INCOME_SOURCE_LABELS: Record<IncomeSource, string> = {
    SALARIO: 'Salary',
    FREELANCE: 'Freelance',
    CONSIGNACIONES: 'Deposits',
    OTROS: 'Other'
}

// El backend guarda UTC pero devuelve "2026-10-24T10:33:59" sin sufijo de zona.
// Sin la Z, JS lo leería como hora local y lo mostraría corrido.
export function parseApiDate(iso: string): Date {
    const hasZone = /(Z|[+-]\d{2}:?\d{2})$/.test(iso)
    return new Date(hasZone ? iso : `${iso}Z`)
}

// Se muestra en la zona horaria del navegador (Colombia en tu caso)
export function formatDateTime(iso: string): string {
    return parseApiDate(iso).toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' })
}

// Date → "2026-10-24T05:30", el formato que pide <input type="datetime-local">
export function toDatetimeLocal(date: Date): string {
    const pad = (n: number) => String(n).padStart(2, '0')
    return (
        `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}` +
        `T${pad(date.getHours())}:${pad(date.getMinutes())}`
    )
}