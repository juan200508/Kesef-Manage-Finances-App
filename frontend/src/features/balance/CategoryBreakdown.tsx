import { Card } from '../../components/ui/Card'
import { Skeleton } from '../../components/ui/Skeleton'
import { formatCurrency } from '../../lib/format'
import type { CategoryTotal } from './utils'

export function CategoryBreakdown({ categories }: { categories: CategoryTotal[] | null }) {
    const max = categories?.[0]?.total ?? 0   // ya viene ordenado: el primero es el mayor

    return (
        <Card className="space-y-4">
            <h2 className="font-semibold">Expenses by category</h2>

            {categories === null && (
                <div className="space-y-3">
                    {[0, 1, 2, 3].map((i) => (
                        <Skeleton key={i} className="h-8 w-full" />
                    ))}
                </div>
            )}

            {categories?.length === 0 && (
                <p className="text-sm text-content-muted">No expenses in this period.</p>
            )}

            {categories && categories.length > 0 && (
                <ul className="space-y-3">
                    {categories.map((c) => (
                        <li key={c.id} className="space-y-1">
                            <div className="flex justify-between text-sm">
                                <span>{c.name}</span>
                                <span className="text-content-muted">{formatCurrency(c.total)}</span>
                            </div>
                            <div className="h-1.5 rounded-full bg-line">
                                <div
                                    className="h-1.5 rounded-full bg-brand"
                                    style={{ width: `${(c.total / max) * 100}%` }}
                                />
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </Card>
    )
}