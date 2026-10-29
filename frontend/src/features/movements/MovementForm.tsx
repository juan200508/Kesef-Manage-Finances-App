import type { ReactNode } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { getErrorMessage } from '../../api/errors'
import { MOVEMENT_TYPES } from '../../api/types'
import { AmountInput } from '../../components/ui/AmountInput'
import type { Category, Movement, MovementType, MovementUpdateInput } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'
import { MOVEMENT_TYPE_LABELS, parseApiDate, toDatetimeLocal, normalizeAmount } from '../../lib/format'
import { useCreateMovement, useUpdateMovement } from './hooks'

interface FormValues {
    movement_type: MovementType
    category_id: string
    amount: string
    description: string
    movement_date: string // formato datetime-local
}

interface Props {
    movement?: Movement // si viene, es edición
    categories: Category[]
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

export function MovementForm({ movement, categories, onClose }: Props) {
    const create = useCreateMovement()
    const update = useUpdateMovement()

    const defaults: FormValues = movement
        ? {
              movement_type: movement.movement_type,
              category_id: movement.category_id,
              amount: normalizeAmount(movement.amount),
              description: movement.description ?? '',
              movement_date: toDatetimeLocal(parseApiDate(movement.movement_date)),
          }
        : {
              movement_type: 'COMPRA',
              category_id: '',
              amount: '',
              description: '',
              movement_date: toDatetimeLocal(new Date()),
          }

    const { register, handleSubmit, control, formState: { errors } } = useForm<FormValues>({ defaultValues: defaults })

    const isPending = create.isPending || update.isPending
    const error = create.error ?? update.error

    const onSubmit = (values: FormValues) => {
        if (!movement) {
            create.mutate(
                {
                    category_id: values.category_id,
                    movement_type: values.movement_type,
                    amount: values.amount,
                    description: values.description || undefined,
                    movement_date: new Date(values.movement_date).toISOString(),
                },
                { onSuccess: onClose },
            )
            return
        }

        // Edición: solo se envía lo que cambió (así no se toca movement_date sin querer)
        const payload: MovementUpdateInput = {}
        if (values.movement_type !== defaults.movement_type) payload.movement_type = values.movement_type
        if (values.category_id !== defaults.category_id) payload.category_id = values.category_id
        if (values.amount !== defaults.amount) payload.amount = values.amount
        if (values.description !== defaults.description) payload.description = values.description || null
        if (values.movement_date !== defaults.movement_date) {
            payload.movement_date = new Date(values.movement_date).toISOString()
        }

        if (Object.keys(payload).length === 0) return onClose()
        update.mutate({ id: movement.id, data: payload }, { onSuccess: onClose })
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
            <Field label="Type">
                <Select {...register('movement_type')}>
                    {MOVEMENT_TYPES.map((t) => (
                        <option key={t} value={t}>{MOVEMENT_TYPE_LABELS[t]}</option>
                    ))}
                </Select>
            </Field>

            <Field label="Category" error={errors.category_id?.message}>
                <Select {...register('category_id', { required: 'Select a category' })}>
                    <option value="">Select a category</option>
                    {categories.map((c) => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                </Select>
            </Field>

            <Field label="Amount (COP)" error={errors.amount?.message}>
                <Controller
                    name="amount"
                    control={control}
                    rules={{
                        required: 'Amount is required',
                        pattern: { value: /^\d{1,10}(\.\d{1,2})?$/, message: 'Up to 10 digits and 2 decimals' },
                        validate: (v) => Number(v) > 0 || 'Must be greater than 0',
                    }}
                    render={({ field }) => (
                        <AmountInput
                            placeholder="0"
                            value={field.value}
                            onChange={field.onChange}
                            onBlur={field.onBlur}
                        />
                    )}
                />
            </Field>

            <Field label="Date and time" error={errors.movement_date?.message}>
                <Input
                    type="datetime-local"
                    {...register('movement_date', { required: 'Date is required' })}
                />
            </Field>

            <Field label="Description (optional)">
                <Input type="text" {...register('description')} />
            </Field>

            {error && <p className="text-sm text-expense">{getErrorMessage(error)}</p>}

            <div className="flex justify-end gap-2 pt-2">
                <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={isPending || categories.length === 0}>
                    {isPending ? 'Saving…' : movement ? 'Save changes' : 'Create'}
                </Button>
            </div>
        </form>
    )
}