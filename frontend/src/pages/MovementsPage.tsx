import { useState } from 'react'
import { getErrorMessage } from '../api/errors'
import type { Movement } from '../api/types'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Modal } from '../components/ui/Modal'
import { useCategories } from '../features/categories/hooks'
import { EMPTY_FILTERS, type MovementFilters as Filters } from '../features/movements/api'
import { useMovements } from '../features/movements/hooks'
import { MovementFilters } from '../features/movements/MovementFilter'
import { MovementForm } from '../features/movements/MovementForm'
import { MovementsTable } from '../features/movements/MovementTable'
import { parseApiDate } from '../lib/format'

export function MovementsPage() {
    const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS)
    // null = cerrado · {} = crear · { movement } = editar
    const [modal, setModal] = useState<{ movement?: Movement } | null>(null)

    const categories = useCategories()
    const movements = useMovements(filters)

    const categoryList = categories.data ?? []
    const categoryNames = new Map(categoryList.map((c) => [c.id, c.name]))

    // El backend ordena por created_at; aquí se ordena por la fecha del movimiento
    const rows = movements.data
        ? [...movements.data].sort(
              (a, b) => parseApiDate(b.movement_date).getTime() - parseApiDate(a.movement_date).getTime(),
          )
        : undefined

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-xl font-semibold">Movements</h1>
                <Button onClick={() => setModal({})}>New movement</Button>
            </div>

            <MovementFilters filters={filters} categories={categoryList} onChange={setFilters} />

            {movements.isError ? (
                <Card className="space-y-3">
                    <p className="text-sm text-expense">{getErrorMessage(movements.error)}</p>
                    <Button variant="ghost" onClick={() => movements.refetch()}>Try again</Button>
                </Card>
            ) : (
                <div className={`transition-opacity ${movements.isFetching ? 'opacity-60' : ''}`}>
                    <MovementsTable
                        movements={rows}
                        categoryNames={categoryNames}
                        onEdit={(movement) => setModal({ movement })}
                    />
                </div>
            )}

            {modal && (
                <Modal
                    title={modal.movement ? 'Edit movement' : 'New movement'}
                    onClose={() => setModal(null)}
                >
                    <MovementForm
                        movement={modal.movement}
                        categories={categoryList}
                        onClose={() => setModal(null)}
                    />
                </Modal>
            )}
        </div>
    )
}