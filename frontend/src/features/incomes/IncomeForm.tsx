import type { ReactNode } from 'react'
import { useForm } from 'react-hook-form'
import { getErrorMessage } from '../../api/errors'
import { INCOME_SOURCE } from '../../api/types'
import type { IncomeSource, IncomeUpdateInput, Income } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'
import { INCOME_SOURCE_LABELS, MONTH_LABELS } from '../../lib/format'
import { useCreateIncome, useUpdateIncome } from './hooks'

// Año y mes viajan como string en el formulario (un <select> siempre devuelve string)
interface FormValues {
    year: string
    month: string
    amount: string
    source: IncomeSource
    description: string
}

interface Props {
    income?: Income // si viene, es edición
    initialYear?: number // valores iniciales al crear
    initialMonth?: number
    onClose: () => void
}

function Field({ label, error, children }: { label: string; error?: string; children: ReactNode }) {
    return (
        <label className="block space-y-1">
            <span className="text-xs text-content-muted">{label}</span>
            {children}
            {error && <p className="text-xs text-expense">{error}</p>}
        </label>
    )
}

export function IncomeForm({ income, initialYear, initialMonth, onClose }: Props) {
    const create = useCreateIncome()
    const update = useUpdateIncome()

    const now = new Date()
    const defaults: FormValues = income
        ? {
              year: String(income.year),
              month: String(income.month),
              amount: income.amount,
              source: income.source,
              description: income.description ?? '',
          }
        : {
              year: String(initialYear ?? now.getFullYear()),
              month: String(initialMonth ?? now.getMonth() + 1),
              amount: '',
              source: 'SALARIO',
              description: '',
          }

    const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({ defaultValues: defaults })

    const isPending = create.isPending || update.isPending
    const error = create.error ?? update.error

    const onSubmit = (values: FormValues) => {
        const description = values.description.trim()

        if (!income) {
            create.mutate(
                {
                    year: Number(values.year),
                    month: Number(values.month),
                    amount: values.amount,
                    source: values.source,
                    description: description || undefined,
                },
                { onSuccess: onClose },
            )
            return
        }

        // Edición: solo se envía lo que cambió
        const payload: IncomeUpdateInput = {}
        if (values.year !== defaults.year) payload.year = Number(values.year)
        if (values.month !== defaults.month) payload.month = Number(values.month)
        if (values.amount !== defaults.amount) payload.amount = values.amount
        if (values.source !== defaults.source) payload.source = values.source
        // El backend exige min_length=1: si se borró el texto, va null (no '')
        if (values.description !== defaults.description) payload.description = description || null

        if (Object.keys(payload).length === 0) return onClose()
        update.mutate({ id: income.id, data: payload }, { onSuccess: onClose })
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
                <Field label="Year" error={errors.year?.message}>
                    <Input
                        type="number"
                        {...register('year', {
                            required: 'Year is required',
                            validate: (v) => {
                                const n = Number(v)
                                return (Number.isInteger(n) && n >= 2000 && n <= 2100) || 'Between 2000 and 2100'
                            },
                        })}
                    />
                </Field>

                <Field label="Month">
                    <Select {...register('month')}>
                        {MONTH_LABELS.map((label, i) => (
                            <option key={label} value={i + 1}>{label}</option>
                        ))}
                    </Select>
                </Field>
            </div>

            <Field label="Source">
                <Select {...register('source')}>
                    {INCOME_SOURCE.map((s) => (
                        <option key={s} value={s}>{INCOME_SOURCE_LABELS[s]}</option>
                    ))}
                </Select>
            </Field>

            <Field label="Amount (COP)" error={errors.amount?.message}>
                <Input
                    type="text"
                    inputMode="decimal"
                    placeholder="0.00"
                    {...register('amount', {
                        required: 'Amount is required',
                        pattern: { value: /^\d{1,10}(\.\d{1,2})?$/, message: 'Up to 10 digits and 2 decimals' },
                        validate: (v) => Number(v) > 0 || 'Must be greater than 0',
                    })}
                />
            </Field>

            <Field label="Description (optional)" error={errors.description?.message}>
                <Input
                    type="text"
                    {...register('description', {
                        maxLength: { value: 255, message: 'At most 255 characters' },
                    })}
                />
            </Field>

            {error && <p className="text-sm text-expense">{getErrorMessage(error)}</p>}

            <div className="flex justify-end gap-2 pt-2">
                <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={isPending}>
                    {isPending ? 'Saving…' : income ? 'Save changes' : 'Create'}
                </Button>
            </div>
        </form>
    )
}