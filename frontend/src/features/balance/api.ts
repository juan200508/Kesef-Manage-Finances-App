import { api } from '../../api/client'
import type { MonthlyBalance } from '../../api/types'

export async function getBalance(year: number, months: number[]) {
    const { data } = await api.get<MonthlyBalance[]>('/balance', {
        params: { year, month: months },
        paramsSerializer: { indexes: null },
    })
    return data
}