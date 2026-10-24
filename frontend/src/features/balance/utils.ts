import type { MonthlyBalance } from '../../api/types'

export interface Summary {
    income: number
    expenses: number
    balance: number
}

export interface CategoryTotal {
    id: string
    name: string
    total: number
}

export function summarize(data: MonthlyBalance[]): Summary {
    return data.reduce<Summary>(
        (acc, m) => ({
            income: acc.income + Number(m.total_income),
            expenses: acc.expenses + Number(m.total_expenses),
            balance: acc.balance + Number(m.balance),
        }),
        { income: 0, expenses: 0, balance: 0 },
    )
}

// Une la misma categoría repetida en varios meses y ordena de mayor a menor
export function mergeCategories(data: MonthlyBalance[]): CategoryTotal[] {
    const totals = new Map<string, CategoryTotal>()

    for (const month of data) {
        for (const c of month.expenses_by_category) {
            const prev = totals.get(c.category_id)
            totals.set(c.category_id, {
                id: c.category_id,
                name: c.category_name,
                total: (prev?.total ?? 0) + Number(c.total),
            })
        }
    }

    return [...totals.values()].sort((a, b) => b.total - a.total)
}