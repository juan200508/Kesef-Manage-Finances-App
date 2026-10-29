import { api } from "../../api/client";
import type { Income, IncomeCreateInput, IncomeUpdateInput } from "../../api/types";

export async function getIncomes(year: number, months: number[]) {
    const { data } = await api.get<Income[]>('monthly_incomes', {
        params: { year, month: months },
        paramsSerializer: { indexes: null }
    })
    return data
}

export async function createIncome(input: IncomeCreateInput) {
    const { data } = await api.post<Income>('monthly_incomes', input)
    return data
}

export async function updateIncome(id: string, input: IncomeUpdateInput) {
    const { data } = await api.put<Income>(`monthly_incomes/${id}`, input)
    return data
}

export async function deleteIncome(id: string) {
    await api.delete<Income>(`monthly_incomes/${id}`)
}