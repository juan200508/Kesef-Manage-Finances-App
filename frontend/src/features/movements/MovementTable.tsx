import { useState } from 'react'
import { getErrorMessage } from '../../api/errors'
import type { Movement } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Skeleton } from '../../components/ui/Skeleton'
import { MOVEMENT_TYPE_LABELS, formatCurrency, formatDateTime } from '../../lib/format'
import { useDeleteMovement } from './hooks'

interface Props {
    movements: Movement[] | undefined // undefined = cargando
    categoryNames: Map<string, string>
    onEdit: (movement: Movement) => void
}

export function MovementsTable({ movements, categoryNames, onEdit }: Props) {
    const [confirmingId, setConfirmingId] = useState<string | null>(null)
    const remove = useDeleteMovement()

    const handleDelete = (id: string) =>
        remove.mutate(id, { onSettled: () => setConfirmingId(null) })

    return (
        <Card className="space-y-3 overflow-x-auto">
            <table className="w-full text-sm">
                <thead className="border-b border-line text-left text-xs text-content-muted">
                    <tr>
                        <th className="px-2 py-2 font-medium">Date</th>
                        <th className="px-2 py-2 font-medium">Description</th>
                        <th className="px-2 py-2 font-medium">Category</th>
                        <th className="px-2 py-2 font-medium">Type</th>
                        <th className="px-2 py-2 text-right font-medium">Amount</th>
                        <th className="px-2 py-2" />
                    </tr>
                </thead>
                <tbody>
                    {movements === undefined &&
                        [0, 1, 2, 3, 4].map((i) => (
                            <tr key={i}>
                                <td colSpan={6} className="px-2 py-2">
                                    <Skeleton className="h-8 w-full" />
                                </td>
                            </tr>
                        ))}

                    {movements?.map((m) => (
                        <tr key={m.id} className="border-b border-line last:border-0">
                            <td className="whitespace-nowrap px-2 py-3 text-content-muted">
                                {formatDateTime(m.movement_date)}
                            </td>
                            <td className="px-2 py-3">{m.description ?? '—'}</td>
                            <td className="px-2 py-3">{categoryNames.get(m.category_id) ?? '—'}</td>
                            <td className="px-2 py-3">
                                <span className="rounded-md border border-line px-2 py-0.5 text-xs text-content-muted">
                                    {MOVEMENT_TYPE_LABELS[m.movement_type]}
                                </span>
                            </td>
                            <td className="whitespace-nowrap px-2 py-3 text-right font-medium">
                                {formatCurrency(m.amount)}
                            </td>
                            <td className="whitespace-nowrap px-2 py-3 text-right">
                                {confirmingId === m.id ? (
                                    <span className="inline-flex items-center gap-1">
                                        <span className="text-xs text-content-muted">Delete?</span>
                                        <Button
                                            variant="danger"
                                            disabled={remove.isPending}
                                            onClick={() => handleDelete(m.id)}
                                        >
                                            Yes
                                        </Button>
                                        <Button variant="ghost" onClick={() => setConfirmingId(null)}>No</Button>
                                    </span>
                                ) : (
                                    <span className="inline-flex gap-1">
                                        <Button variant="ghost" onClick={() => onEdit(m)}>Edit</Button>
                                        <Button variant="ghost" onClick={() => setConfirmingId(m.id)}>Delete</Button>
                                    </span>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {movements?.length === 0 && (
                <p className="py-4 text-center text-sm text-content-muted">
                    No movements match these filters.
                </p>
            )}

            {remove.isError && <p className="text-sm text-expense">{getErrorMessage(remove.error)}</p>}
        </Card>
    )
}