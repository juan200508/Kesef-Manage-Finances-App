import { useState } from 'react'
import { getErrorMessage } from '../api/errors'
import type { Category } from '../api/types'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Modal } from '../components/ui/Modal'
import { CategoryForm } from '../features/categories/CategoryForm'
import { CategoryList } from '../features/categories/CategortList'
import { useCategories } from '../features/categories/hooks'

export function CategoriesPage() {
    // null = cerrado · {} = crear · { category } = editar
    const [modal, setModal] = useState<{ category?: Category } | null>(null)
    const { data, isError, error, refetch } = useCategories()

    return (
        <div className="space-y-6">
            <title>Categories · Kesef</title>
            <div className="flex items-center justify-between">
                <h1 className="text-xl font-semibold">Categories</h1>
                <Button onClick={() => setModal({})}>New category</Button>
            </div>

            {isError ? (
                <Card className="space-y-3">
                    <p className="text-sm text-expense">{getErrorMessage(error)}</p>
                    <Button variant="ghost" onClick={() => refetch()}>Try again</Button>
                </Card>
            ) : (
                <CategoryList categories={data} onEdit={(category) => setModal({ category })} />
            )}

            {modal && (
                <Modal
                    title={modal.category ? 'Edit category' : 'New category'}
                    onClose={() => setModal(null)}
                >
                    <CategoryForm category={modal.category} onClose={() => setModal(null)} />
                </Modal>
            )}
        </div>
    )
}