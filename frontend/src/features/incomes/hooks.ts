import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type { IncomeUpdateInput } from '../../api/types'
import {
    getIncomes,
    createIncome,
    updateIncome,
    deleteIncome
} from './api'

export function useIncomes(year: number, months: number[]) {
    return useQuery({
        queryKey: ['incomes', year, months],
        queryFn: () => getIncomes(year, months),
        placeholderData: keepPreviousData
    })
}

function useRefreshIncomeData() {
    const queryClient = useQueryClient()
    return () => {
        queryClient.invalidateQueries({ queryKey: ['incomes'] })
        queryClient.invalidateQueries({ queryKey: ['balance'] })
    }
}

export function useCreateIncome() {
    const refresh = useRefreshIncomeData
    return useMutation({ mutationFn: createIncome, onSuccess: refresh })
}

export function useUpdateIncome() {
    const refresh = useRefreshIncomeData()
    return useMutation({
        mutationFn: ({ id, data }: {id: string; data: IncomeUpdateInput}) => updateIncome(id, data),
        onSuccess: refresh
    })
}

export function useDeleteIncome() {
    const refresh = useRefreshIncomeData
    return useMutation({mutationFn: deleteIncome, onSuccess: refresh})
}

