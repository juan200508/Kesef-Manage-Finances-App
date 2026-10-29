import { useState } from 'react'
import { getErrorMessage } from '../../api/errors'
import type { Income } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Modal } from '../../components/ui/Modal'
import { INCOME_SOURCE_LABELS, MONTH_LABELS, formatCurrency } from '../../lib/format'
import { useDeleteIncome } from './hooks'
import type { IncomeGroup } from './utils'

interface Props {
    group: IncomeGroup
    onEdit: (income: Income) => void
    onClose: () => void
}

export function IncomeDetailModal({ group, onEdit, onClose }: Props) {
    const [confirmingId, setConfirmingId] = useState<string | null>(null)
    const remove = useDeleteIncome()

    const handleDelete = (id: string) =>
        remove.mutate(id, {
            onSuccess: () => {
                // Si era el último ingreso del grupo, el grupo desaparece: se cierra el modal
                if (group.items.length === 1) onClose()
            },
            onSettled: () => setConfirmingId(null),
        })

    return (
        <Modal title={INCOME_SOURCE_LABELS[group.source]} onClose={onClose} className="max-w-xl">
            <p className="text-sm text-content-muted">
                {group.count} {group.count === 1 ? 'entry' : 'entries'} · {formatCurrency(group.total)}
            </p>

            <ul className="divide-y divide-line">
                {group.items.map((income) => (
                    <li key={income.id} className="flex items-center justify-between gap-3 py-3">
                        <div className="min-w-0">
                            <p className="text-sm font-medium">
                                {MONTH_LABELS[income.month - 1]} {income.year}
                            </p>
                            <p className="truncate text-xs text-content-muted">{income.description ?? '—'}</p>
                        </div>

                        <div className="flex shrink-0 items-center gap-3">
                            <span className="text-sm font-medium">{formatCurrency(income.amount)}</span>

                            {confirmingId === income.id ? (
                                <span className="inline-flex items-center gap-1">
                                    <span className="text-xs text-content-muted">Delete?</span>
                                    <Button
                                        variant="danger"
                                        disabled={remove.isPending}
                                        onClick={() => handleDelete(income.id)}
                                    >
                                        Yes
                                    </Button>
                                    <Button variant="ghost" onClick={() => setConfirmingId(null)}>No</Button>
                                </span>
                            ) : (
                                <span className="inline-flex gap-1">
                                    <Button variant="ghost" onClick={() => onEdit(income)}>Edit</Button>
                                    <Button variant="ghost" onClick={() => setConfirmingId(income.id)}>Delete</Button>
                                </span>
                            )}
                        </div>
                    </li>
                ))}
            </ul>

            {remove.isError && <p className="text-sm text-expense">{getErrorMessage(remove.error)}</p>}

            <div className="flex justify-end">
                <Button variant="ghost" onClick={onClose}>Close</Button>
            </div>
        </Modal>
    )
}