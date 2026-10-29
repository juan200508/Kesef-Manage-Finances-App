import type { IncomeSource, Income } from '../../api/types'

export interface IncomeGroup {
    source: IncomeSource
    total: number
    count: number
    items: Income[]
}

// Más reciente primero: año, luego mes y, si empatan, fecha de creación
function compareIncomes(a: Income, b: Income) {
    return b.year - a.year || b.month - a.month || b.created_at.localeCompare(a.created_at)
}

// Agrupa los ingresos por fuente. Cada grupo conserva sus ingresos para el pop-up de detalle.
export function groupBySource(incomes: Income[]): IncomeGroup[] {
    const groups = new Map<IncomeSource, IncomeGroup>()

    for (const income of incomes) {
        const group = groups.get(income.source) ?? {
            source: income.source,
            total: 0,
            count: 0,
            items: [],
        }
        group.total += Number(income.amount)
        group.count += 1
        group.items.push(income)
        groups.set(income.source, group)
    }

    for (const group of groups.values()) {
        group.items.sort(compareIncomes)
    }

    // El grupo con más plata primero
    return [...groups.values()].sort((a, b) => b.total - a.total)
}

// Total general del periodo
export function totalIncome(incomes: Income[]): number {
    return incomes.reduce((sum, income) => sum + Number(income.amount), 0)
}