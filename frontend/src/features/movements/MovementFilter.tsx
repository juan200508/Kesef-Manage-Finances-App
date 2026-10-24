import type { Category } from '../../api/types'
import { MOVEMENT_TYPES } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Chip } from '../../components/ui/Chip'
import { Input } from '../../components/ui/Input'
import { MOVEMENT_TYPE_LABELS } from '../../lib/format'
import { EMPTY_FILTERS, type MovementFilters as Filters } from './api'

interface Props {
    filters: Filters
    categories: Category[]
    onChange: (filters: Filters) => void
}

const toggle = <T,>(list: T[], item: T) =>
    list.includes(item) ? list.filter((x) => x !== item) : [...list, item]

export function MovementFilters({ filters, categories, onChange }: Props) {
    return (
        <Card className="space-y-4">
            <div className="flex flex-wrap items-center gap-2">
                <span className="w-20 text-xs text-content-muted">Type</span>
                {MOVEMENT_TYPES.map((t) => (
                    <Chip
                        key={t}
                        active={filters.types.includes(t)}
                        onClick={() => onChange({ ...filters, types: toggle(filters.types, t) })}
                    >
                        {MOVEMENT_TYPE_LABELS[t]}
                    </Chip>
                ))}
            </div>

            <div className="flex flex-wrap items-center gap-2">
                <span className="w-20 text-xs text-content-muted">Category</span>
                {categories.map((c) => (
                    <Chip
                        key={c.id}
                        active={filters.categoryIds.includes(c.id)}
                        onClick={() => onChange({ ...filters, categoryIds: toggle(filters.categoryIds, c.id) })}
                    >
                        {c.name}
                    </Chip>
                ))}
            </div>

            <div className="flex flex-wrap items-end gap-3">
                <label className="space-y-1">
                    <span className="block text-xs text-content-muted">From</span>
                    <Input
                        type="date"
                        value={filters.from}
                        onChange={(e) => onChange({ ...filters, from: e.target.value })}
                    />
                </label>
                <label className="space-y-1">
                    <span className="block text-xs text-content-muted">To</span>
                    <Input
                        type="date"
                        value={filters.to}
                        onChange={(e) => onChange({ ...filters, to: e.target.value })}
                    />
                </label>
                <Button variant="ghost" onClick={() => onChange(EMPTY_FILTERS)}>Clear filters</Button>
            </div>
        </Card>
    )
}