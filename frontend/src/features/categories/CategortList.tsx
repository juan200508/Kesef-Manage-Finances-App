import { useState } from 'react'
import { getErrorMessage } from '../../api/errors'
import type { Category } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { Skeleton } from '../../components/ui/Skeleton'
import { useDeleteCategory } from './hooks'

interface Props {
    categories: Category[] | undefined // undefined = cargando
    onEdit: (category: Category) => void
}

function SkeletonRows() {
    return (
        <div className="space-y-2">
            {[0, 1, 2].map((i) => (
                <Skeleton key={i} className="h-9 w-full" />
            ))}
        </div>
    )
}

export function CategoryList({ categories, onEdit }: Props) {
    const [confirmingId, setConfirmingId] = useState<string | null>(null)
    const remove = useDeleteCategory()

    const globals = categories?.filter((c) => c.is_global)
    const personals = categories?.filter((c) => !c.is_global)

    const handleDelete = (id: string) =>
        remove.mutate(id, { onSettled: () => setConfirmingId(null) })

    return (
        <div className="grid gap-6 md:grid-cols-2">
            {/* Personales: editables */}
            <Card className="space-y-3">
                <h2 className="font-semibold">Your categories</h2>

                {personals === undefined && <SkeletonRows />}

                {personals?.length === 0 && (
                    <p className="text-sm text-content-muted">You haven't created any categories yet.</p>
                )}

                {personals && personals.length > 0 && (
                    <ul className="divide-y divide-line">
                        {personals.map((c) => (
                            <li key={c.id} className="flex flex-wrap items-center justify-between gap-2 py-2">
                                <span className="text-sm">{c.name}</span>

                                {confirmingId === c.id ? (
                                    <span className="inline-flex flex-wrap items-center gap-1">
                                        <span className="text-xs text-content-muted">
                                            Its movements will move to “Otros”. Delete?
                                        </span>
                                        <Button
                                            variant="danger"
                                            disabled={remove.isPending}
                                            onClick={() => handleDelete(c.id)}
                                        >
                                            Yes
                                        </Button>
                                        <Button variant="ghost" onClick={() => setConfirmingId(null)}>No</Button>
                                    </span>
                                ) : (
                                    <span className="inline-flex gap-1">
                                        <Button variant="ghost" onClick={() => onEdit(c)}>Edit</Button>
                                        <Button variant="ghost" onClick={() => setConfirmingId(c.id)}>Delete</Button>
                                    </span>
                                )}
                            </li>
                        ))}
                    </ul>
                )}

                {remove.isError && <p className="text-sm text-expense">{getErrorMessage(remove.error)}</p>}
            </Card>

            {/* Globales: solo lectura */}
            <Card className="space-y-3">
                <h2 className="font-semibold">Default categories</h2>

                {globals === undefined && <SkeletonRows />}

                {globals && (
                    <ul className="divide-y divide-line">
                        {globals.map((c) => (
                            <li key={c.id} className="flex items-center justify-between py-2">
                                <span className="text-sm">{c.name}</span>
                                <span className="rounded-md border border-line px-2 py-0.5 text-xs text-content-muted">
                                    Shared
                                </span>
                            </li>
                        ))}
                    </ul>
                )}
            </Card>
        </div>
    )
}