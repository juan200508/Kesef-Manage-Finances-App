import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { MONTH_LABELS } from '../../lib/format'

interface Props {
    year: number
    months: number[]
    onYearChange: (year: number) => void
    onToggleMonth: (month: number) => void
    onClearMonths: () => void
}

export function FilterBar({ year, months, onYearChange, onToggleMonth, onClearMonths }: Props) {
    return (
        <Card className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
                <Button variant="ghost" onClick={() => onYearChange(year - 1)}>←</Button>
                <span className="w-16 text-center font-semibold">{year}</span>
                <Button variant="ghost" onClick={() => onYearChange(year + 1)}>→</Button>
            </div>

            <div className="flex flex-wrap gap-1.5">
                {MONTH_LABELS.map((label, i) => {
                    const month = i + 1
                    const active = months.includes(month)
                    return (
                        <button
                            key={month}
                            type="button"
                            onClick={() => onToggleMonth(month)}
                            className={
                                'cursor-pointer rounded-lg px-3 py-1.5 text-sm transition-colors ' +
                                (active
                                    ? 'bg-brand text-on-brand'
                                    : 'border border-line text-content-muted hover:text-content')
                            }
                        >
                            {label}
                        </button>
                    )
                })}
            </div>

            <Button variant="ghost" onClick={onClearMonths}>Whole year</Button>
        </Card>
    )
}