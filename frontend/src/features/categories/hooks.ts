import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type { CategoryInput } from '../../api/types'
import { createCategory, deleteCategory, getCategories, updateCategory } from './api'
import { useToast } from '../../components/ui/toast-context'

export function useCategories() {
    return useQuery({
        queryKey: ['categories'],
        queryFn: getCategories,
        staleTime: 5 * 60 * 1000, // las categorías cambian poco
    })
}

function useInvalidate() {
    const queryClient = useQueryClient()
    return (...keys: string[]) => keys.forEach((key) => queryClient.invalidateQueries({ queryKey: [key] }))
}

export function useCreateCategory() {
    const invalidate = useInvalidate()
    const toast = useToast()
    return useMutation({
        mutationFn: createCategory,
        onSuccess: () => {
            invalidate('categories'),
            toast.success('Category created')
        },
    })
}

export function useUpdateCategory() {
    const invalidate = useInvalidate()
    const toast = useToast()
    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: CategoryInput }) => updateCategory(id, data),
        // El nombre también aparece en el desglose del balance
        onSuccess: () => {
            invalidate('categories', 'balance'),
            toast.success('Category updated')
        },
    })
}

export function useDeleteCategory() {
    const invalidate = useInvalidate()
    const toast = useToast()
    return useMutation({
        mutationFn: deleteCategory,
        // Los movimientos de la categoría borrada pasan a "Otros"
        onSuccess: () => {
            invalidate('categories', 'balance', 'movements'),
            toast.success('Category deleted')
        },
    })
}