import { Card } from '../../components/ui/Card'
import { Skeleton } from '../../components/ui/Skeleton'
import { formatCurrency } from '../../lib/format'
import type { Summary } from './utils'

interface StatProps {
    label: string
    value?: number
    className?: string
}

function Stat({ label, value, className = '' }: StatProps) {
    return (
        <Card className="space-y-2">
            <p className="text-sm text-content-muted">{label}</p>
            {value === undefined ? (
                <Skeleton className="h-8 w-36" />
            ) : (
                <p className={`text-2xl font-semibold ${className}`}>{formatCurrency(value)}</p>
            )}
        </Card>
    )
}

export function SummaryCards({ summary }: { summary: Summary | null }) {
    return (
        <div className="grid gap-4 sm:grid-cols-3">
            <Stat label="Income" value={summary?.income} className="text-income" />
            <Stat label="Expenses" value={summary?.expenses} className="text-expense" />
            <Stat
                label="Balance"
                value={summary?.balance}
                className={summary && summary.balance < 0 ? 'text-expense' : 'text-income'}
            />
        </div>
    )
}