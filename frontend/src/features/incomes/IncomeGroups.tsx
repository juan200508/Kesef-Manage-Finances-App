import type { IncomeSource } from '../../api/types'
import { Card } from '../../components/ui/Card'
import { Skeleton } from '../../components/ui/Skeleton'
import { INCOME_SOURCE_LABELS, formatCurrency } from '../../lib/format'
import type { IncomeGroup } from './utils'

interface Props {
    groups: IncomeGroup[] | null // null = cargando
    onSelect: (source: IncomeSource) => void
}

const GRID = 'grid gap-4 sm:grid-cols-2'

export function IncomeGroups({ groups, onSelect }: Props) {
    if (groups === null) {
        return (
            <div className={GRID}>
                {[0, 1, 2, 3].map((i) => (
                    // Misma estructura que una tarjeta real, para que no salte el diseño
                    <Card key={i} className="space-y-3">
                        <Skeleton className="h-5 w-24" />
                        <Skeleton className="h-8 w-40" />
                        <Skeleton className="h-1.5 w-full" />
                    </Card>
                ))}
            </div>
        )
    }

    if (groups.length === 0) {
        return (
            <Card>
                <p className="text-sm text-content-muted">No income in this period.</p>
            </Card>
        )
    }

    const grandTotal = groups.reduce((sum, g) => sum + g.total, 0)

    return (
        <div className={GRID}>
            {groups.map((group) => {
                const share = grandTotal > 0 ? (group.total / grandTotal) * 100 : 0

                return (
                    <Card
                        key={group.source}
                        onClick={() => onSelect(group.source)}
                        className="cursor-pointer space-y-3 transition-colors hover:border-brand"
                    >
                        <div className="flex justify-between text-sm">
                            <span>{INCOME_SOURCE_LABELS[group.source]}</span>
                            <span className="text-content-muted">
                                {group.count} {group.count === 1 ? 'entry' : 'entries'}
                            </span>
                        </div>

                        <p className="text-2xl font-semibold text-income">{formatCurrency(group.total)}</p>

                        <div className="h-1.5 rounded-full bg-line">
                            <div className="h-1.5 rounded-full bg-brand" style={{ width: `${share}%` }} />
                        </div>
                    </Card>
                )
            })}
        </div>
    )
}