import { useLayoutEffect, useRef } from 'react'
import type { ChangeEvent, ComponentProps } from 'react'
import { formatAmountInput, parseAmountInput } from '../../lib/format'
import { Input } from './Input'

interface Props extends Omit<ComponentProps<'input'>, 'value' | 'onChange' | 'type'> {
    value: string // valor interno: "1500000" o "1500000.5"
    onChange: (value: string) => void
}

export function AmountInput({ value, onChange, onBlur, ...props }: Props) {
    const inputRef = useRef<HTMLInputElement>(null)
    const pendingCaret = useRef<number | null>(null)

    // Después de reformatear, devuelve el cursor a donde estaba
    useLayoutEffect(() => {
        if (pendingCaret.current === null) return
        inputRef.current?.setSelectionRange(pendingCaret.current, pendingCaret.current)
        pendingCaret.current = null
    })

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const input = e.target
        const caret = input.selectionStart ?? input.value.length
        // Cuántos dígitos (o comas) había a la izquierda del cursor
        const significantBefore = input.value.slice(0, caret).replace(/[^\d,]/g, '').length

        const raw = parseAmountInput(input.value)
        const formatted = formatAmountInput(raw)

        // Posición en el texto formateado que tiene esos mismos caracteres a la izquierda
        let seen = 0
        let pos = 0
        while (pos < formatted.length && seen < significantBefore) {
            if (/[\d,]/.test(formatted[pos])) seen++
            pos++
        }
        pendingCaret.current = pos

        onChange(raw)
    }

    return (
        <Input
            ref={inputRef}
            type="text"
            inputMode="decimal"
            value={formatAmountInput(value)}
            onChange={handleChange}
            onBlur={(e) => {
                // "1500," al salir del campo queda "1500"
                if (value.endsWith('.')) onChange(value.slice(0, -1))
                onBlur?.(e)
            }}
            {...props}
        />
    )
}