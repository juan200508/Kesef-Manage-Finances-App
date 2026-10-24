import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { getBalance } from './api'

export function useBalance(year: number, months: number[]) {
    return useQuery({
        queryKey: ['balance', year, months],
        queryFn: () => getBalance(year, months),
        // Al cambiar un filtro se conservan los datos anteriores mientras llegan los nuevos
        placeholderData: keepPreviousData,
    })
}