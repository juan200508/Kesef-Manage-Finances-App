import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type { MovementUpdateInput } from '../../api/types'
import { useToast } from '../../components/ui/toast-context'
import {
    createMovement,
    deleteMovement,
    getMovements,
    updateMovement,
    type MovementFilters,
} from './api'

export function useMovements(filters: MovementFilters) {
    return useQuery({
        queryKey: ['movements', filters],
        queryFn: () => getMovements(filters),
        placeholderData: keepPreviousData,
    })
}

// Un cambio en movimientos altera listado y balance: se invalidan ambos
function useRefreshMovementData() {
    const queryClient = useQueryClient()
    return () => {
        queryClient.invalidateQueries({ queryKey: ['movements'] })
        queryClient.invalidateQueries({ queryKey: ['balance'] })
    }
}

export function useCreateMovement() {
    const refresh = useRefreshMovementData()
    const toast = useToast()
    return useMutation({ 
        mutationFn: createMovement, 
        onSuccess: () => {
            refresh()
            toast.success('Movement created')
        }
    })
}

export function useUpdateMovement() {
    const refresh = useRefreshMovementData()
    const toast = useToast()
    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: MovementUpdateInput }) => updateMovement(id, data),
        onSuccess: () => {
            refresh()
            toast.success('Movement updated')
        },
    })
}

export function useDeleteMovement() {
    const refresh = useRefreshMovementData()
    const toast = useToast()
    return useMutation({ 
        mutationFn: deleteMovement, 
        onSuccess: () => {
            refresh()
            toast.success('Movement deleted')
        }
    })
}