import { useForm } from 'react-hook-form'
import { getErrorMessage } from '../../api/errors'
import type { Category } from '../../api/types'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { useCreateCategory, useUpdateCategory } from './hooks'

interface FormValues {
    name: string
}

interface Props {
    category?: Category // si viene, es edición
    onClose: () => void
}

export function CategoryForm({ category, onClose }: Props) {
    const create = useCreateCategory()
    const update = useUpdateCategory()

    const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
        defaultValues: { name: category?.name ?? '' },
    })

    const isPending = create.isPending || update.isPending
    const error = create.error ?? update.error

    const onSubmit = ({ name }: FormValues) => {
        const data = { name: name.trim() }

        if (!category) {
            create.mutate(data, { onSuccess: onClose })
            return
        }

        if (data.name === category.name) return onClose() // nada que guardar
        update.mutate({ id: category.id, data }, { onSuccess: onClose })
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
            <label className="block space-y-1">
                <span className="text-xs text-content-muted">Name</span>
                <Input
                    type="text"
                    autoFocus
                    {...register('name', {
                        validate: (v) => v.trim().length > 0 || 'Name is required',
                        maxLength: { value: 50, message: 'At most 50 characters' },
                    })}
                />
                {errors.name && <p className="text-xs text-expense">{errors.name.message}</p>}
            </label>

            {error && <p className="text-sm text-expense">{getErrorMessage(error)}</p>}

            <div className="flex justify-end gap-2 pt-2">
                <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={isPending}>
                    {isPending ? 'Saving…' : category ? 'Save changes' : 'Create'}
                </Button>
            </div>
        </form>
    )
}