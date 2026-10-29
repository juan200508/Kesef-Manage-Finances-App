import { useState } from 'react'
import { getErrorMessage } from '../api/errors'
import type { IncomeSource, Income } from '../api/types'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Modal } from '../components/ui/Modal'
import { Skeleton } from '../components/ui/Skeleton'
import { FilterBar } from '../features/balance/FilterBar'
import { useIncomes } from '../features/incomes/hooks'
import { IncomeDetailModal } from '../features/incomes/IncomeDetailModal'
import { IncomeForm } from '../features/incomes/IncomeForm'
import { IncomeGroups } from '../features/incomes/IncomeGroups'
import { groupBySource, totalIncome } from '../features/incomes/utils'
import { formatCurrency } from '../lib/format'

type ModalState =
    | { view: 'form'; income?: Income } // sin income = crear
    | { view: 'detail'; source: IncomeSource }
    | null

export function IncomesPage() {
    const now = new Date()
    const [year, setYear] = useState(now.getFullYear())
    const [months, setMonths] = useState<number[]>([now.getMonth() + 1])
    const [modal, setModal] = useState<ModalState>(null)

    const { data, isError, error, isFetching, refetch } = useIncomes(year, months)

    const toggleMonth = (month: number) =>
        setMonths((prev) =>
            prev.includes(month)
                ? prev.filter((m) => m !== month)
                : [...prev, month].sort((a, b) => a - b),
        )

    const groups = data ? groupBySource(data) : null
    const total = data ? totalIncome(data) : null

    // El grupo del detalle se busca en los datos vivos; si ya no existe, no se muestra
    const detailGroup =
        modal?.view === 'detail' ? groups?.find((g) => g.source === modal.source) : undefined

    const closeModal = () => setModal(null)

    return (
        <div className="space-y-6">
            <title>Incomes · Kesef</title>
            <div className="flex items-center justify-between">
                <h1 className="text-xl font-semibold">Incomes</h1>
                <Button onClick={() => setModal({ view: 'form' })}>New income</Button>
            </div>

            <FilterBar
                year={year}
                months={months}
                onYearChange={setYear}
                onToggleMonth={toggleMonth}
                onClearMonths={() => setMonths([])}
            />

            {isError ? (
                <Card className="space-y-3">
                    <p className="text-sm text-expense">{getErrorMessage(error)}</p>
                    <Button variant="ghost" onClick={() => refetch()}>Try again</Button>
                </Card>
            ) : (
                <div className={`space-y-6 transition-opacity ${isFetching ? 'opacity-60' : ''}`}>
                    <Card className="space-y-2">
                        <p className="text-sm text-content-muted">Total income</p>
                        {total === null ? (
                            <Skeleton className="h-8 w-40" />
                        ) : (
                            <p className="text-2xl font-semibold text-income">{formatCurrency(total)}</p>
                        )}
                    </Card>

                    <IncomeGroups
                        groups={groups}
                        onSelect={(source) => setModal({ view: 'detail', source })}
                    />
                </div>
            )}

            {modal?.view === 'form' && (
                <Modal title={modal.income ? 'Edit income' : 'New income'} onClose={closeModal}>
                    <IncomeForm
                        income={modal.income}
                        initialYear={year}
                        initialMonth={months.length === 1 ? months[0] : undefined}
                        onClose={closeModal}
                    />
                </Modal>
            )}

            {detailGroup && (
                <IncomeDetailModal
                    group={detailGroup}
                    onEdit={(income) => setModal({ view: 'form', income })}
                    onClose={closeModal}
                />
            )}
        </div>
    )
}