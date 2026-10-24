import { useState } from 'react'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { getErrorMessage } from '../api/errors'
import { CategoryBreakdown } from '../features/balance/CategoryBreakdown'
import { FilterBar } from '../features/balance/FilterBar'
import { SummaryCards } from '../features/balance/SummaryCards'
import { useBalance } from '../features/balance/hooks'
import { mergeCategories, summarize } from '../features/balance/utils'

export function DashboardPage() {
    const now = new Date()
    const [year, setYear] = useState(now.getFullYear())
    const [months, setMonths] = useState<number[]>([now.getMonth() + 1])

    const { data, isError, error, isFetching, refetch } = useBalance(year, months)

    const toggleMonth = (month: number) =>
        setMonths((prev) =>
            prev.includes(month)
                ? prev.filter((m) => m !== month)
                : [...prev, month].sort((a, b) => a - b),
        )

    const summary = data ? summarize(data) : null
    const categories = data ? mergeCategories(data) : null

    return (
        <div className="space-y-6">
            <FilterBar
                year={year}
                months={months}
                onYearChange={setYear}
                onToggleMonth={toggleMonth}
                onClearMonths={() => setMonths([])}
            />

            {isError ? (
                <Card className="space-y-3">
                    <p className="text-sm text-expense">{getErrorMessage(error)}</p>
                    <Button variant="ghost" onClick={() => refetch()}>Try again</Button>
                </Card>
            ) : data?.length === 0 ? (
                <Card>
                    <p className="text-sm text-content-muted">There is no data for {year} yet.</p>
                </Card>
            ) : (
                <div className={`space-y-6 transition-opacity ${isFetching ? 'opacity-60' : ''}`}>
                    <SummaryCards summary={summary} />
                    <CategoryBreakdown categories={categories} />
                </div>
            )}
        </div>
    )
}