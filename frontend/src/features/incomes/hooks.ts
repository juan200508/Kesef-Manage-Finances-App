import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type { IncomeUpdateInput } from '../../api/types'
import { useToast } from '../../components/ui/toast-context'
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
    const refresh = useRefreshIncomeData()
    const toast = useToast()
    return useMutation({ 
        mutationFn: createIncome, 
        onSuccess: () => {
            refresh()
            toast.success('Income created')
        } 
    })
}

export function useUpdateIncome() {
    const refresh = useRefreshIncomeData()
    const toast = useToast()
    return useMutation({
        mutationFn: ({ id, data }: {id: string; data: IncomeUpdateInput}) => updateIncome(id, data),
        onSuccess: () => {
            refresh()
            toast.success('Income updated')
        } 
    })
}

export function useDeleteIncome() {
    const refresh = useRefreshIncomeData()
    const toast = useToast()
    return useMutation({
        mutationFn: deleteIncome, 
        onSuccess: () => {
            refresh()
            toast.success('Income deleted')
        }
    })
}

