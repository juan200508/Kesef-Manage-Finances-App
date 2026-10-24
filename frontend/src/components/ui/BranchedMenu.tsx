import { useLayoutEffect, useRef, useState } from 'react'
import type { CSSProperties, ReactNode } from 'react'
import './BranchedMenu.css'

export interface MenuLeaf {
    value: string // la ruta, p. ej. '/movements'
    label: string
    icon?: ReactNode // solo se muestra en los hijos de un grupo
}

export interface MenuGroup {
    label: string
    children: MenuLeaf[]
}

export type MenuItem = MenuLeaf | MenuGroup

const isGroup = (item: MenuItem): item is MenuGroup => 'children' in item

const PAD = 6
const MARK = 16

interface Props {
    items: MenuItem[]
    active: string
    onSelect: (value: string) => void
    width?: number
    rowHeight?: number
    indent?: number
    trunk?: number
    radius?: number
    lineWidth?: number
    fontSize?: number
    drawDuration?: number
    foldDuration?: number
    className?: string
}

export function BranchedMenu({
    items,
    active,
    onSelect,
    width = 240,
    rowHeight = 36,
    indent = 40,
    trunk = 14,
    radius = 10,
    lineWidth = 1.5,
    fontSize = 14,
    drawDuration = 400,
    foldDuration = 300,
    className = '',
}: Props) {
    // Todos los grupos abiertos al inicio
    const [open, setOpen] = useState<Set<number>>(
        () => new Set(items.flatMap((item, i) => (isGroup(item) ? [i] : []))),
    )
    const navRef = useRef<HTMLElement>(null)
    const heads = useRef<(HTMLButtonElement | null)[]>([])
    const markerRef = useRef<HTMLSpanElement>(null)

    const activeSection = items.findIndex(
        (item) => isGroup(item) && item.children.some((kid) => kid.value === active),
    )
    const markerShown = activeSection >= 0 && open.has(activeSection)

    // Coloca el indicador de la izquierda junto al grupo activo
    useLayoutEffect(() => {
        const place = (glide: boolean) => {
            const marker = markerRef.current
            const head = heads.current[activeSection] ?? null
            if (!marker) return
            if (!glide) marker.style.transition = 'none'
            if (markerShown && head) {
                marker.style.top = `${head.offsetTop + (head.offsetHeight - MARK) / 2}px`
            }
            marker.toggleAttribute('data-on', markerShown && head !== null)
            if (!glide) {
                void marker.offsetHeight
                marker.style.transition = ''
            }
        }

        place(true)
        let first = true
        const observer = new ResizeObserver(() => {
            if (first) {
                first = false
                return
            }
            place(false)
        })
        if (navRef.current) observer.observe(navRef.current)
        return () => observer.disconnect()
    }, [activeSection, markerShown, items, fontSize, rowHeight])

    const toggle = (i: number) =>
        setOpen((prev) => {
            const next = new Set(prev)
            if (next.has(i)) next.delete(i)
            else next.add(i)
            return next
        })

    // Geometría de las ramas del árbol (SVG)
    const r = Math.min(radius, rowHeight / 2 - 2)
    const endX = indent - 8
    const rowY = (k: number) => PAD + k * rowHeight + rowHeight / 2
    const branch = (k: number) =>
        `M ${trunk} ${rowY(k) - r} A ${r} ${r} 0 0 0 ${trunk + r} ${rowY(k)} H ${endX}`
    const reach = (k: number) =>
        `M ${trunk} 0 V ${rowY(k) - r} A ${r} ${r} 0 0 0 ${trunk + r} ${rowY(k)} H ${endX}`
    const length = (k: number) => rowY(k) - r + (Math.PI * r) / 2 + (endX - trunk - r)

    const style = {
        '--bm-w': `${width}px`,
        '--bm-font': `${fontSize}px`,
        '--bm-row': `${rowHeight}px`,
        '--bm-indent': `${indent}px`,
        '--bm-line-w': lineWidth,
        '--bm-draw': `${drawDuration}ms`,
        '--bm-fold': `${foldDuration}ms`,
    } as CSSProperties

    return (
        <nav
            ref={navRef}
            className={`branched-menu${className ? ` ${className}` : ''}`}
            style={style}
        >
            <span ref={markerRef} className="branched-menu__marker" aria-hidden="true" />

            {items.map((item, i) => {
                const kids = isGroup(item) ? item.children : undefined
                const leafValue = isGroup(item) ? undefined : item.value
                const isOpen = kids ? open.has(i) : false
                const leafActive = leafValue !== undefined && leafValue === active
                const bodyH = kids ? PAD * 2 + kids.length * rowHeight : 0

                return (
                    <div
                        key={isGroup(item) ? item.label : item.value}
                        className="branched-menu__section"
                        data-open={isOpen ? '' : undefined}
                    >
                        <button
                            ref={(el) => {
                                heads.current[i] = el
                            }}
                            type="button"
                            className="branched-menu__head"
                            aria-expanded={kids ? isOpen : undefined}
                            aria-current={leafActive ? 'true' : undefined}
                            data-active={leafActive ? '' : undefined}
                            onClick={() => (leafValue === undefined ? toggle(i) : onSelect(leafValue))}
                        >
                            {item.label}
                        </button>

                        {kids && (
                            <div className="branched-menu__body">
                                <div className="branched-menu__fold">
                                    <div className="branched-menu__tree" style={{ height: bodyH }}>
                                        <svg
                                            className="branched-menu__lines"
                                            width={indent}
                                            height={bodyH}
                                            aria-hidden="true"
                                        >
                                            <path
                                                className="branched-menu__base"
                                                d={`M ${trunk} 0 V ${rowY(kids.length - 1) - r}`}
                                            />
                                            {kids.map((kid, k) => (
                                                <path key={kid.value} className="branched-menu__base" d={branch(k)} />
                                            ))}
                                            {kids.map((kid, k) => (
                                                <path
                                                    key={kid.value}
                                                    className="branched-menu__reach"
                                                    d={reach(k)}
                                                    style={{
                                                        strokeDasharray: length(k),
                                                        strokeDashoffset: kid.value === active ? 0 : length(k),
                                                    }}
                                                />
                                            ))}
                                        </svg>

                                        {kids.map((kid) => (
                                            <button
                                                key={kid.value}
                                                type="button"
                                                className="branched-menu__item"
                                                aria-current={kid.value === active ? 'true' : undefined}
                                                data-active={kid.value === active ? '' : undefined}
                                                tabIndex={isOpen ? 0 : -1}
                                                onClick={() => onSelect(kid.value)}
                                            >
                                                {kid.icon && (
                                                    <span className="branched-menu__icon" aria-hidden="true">
                                                        {kid.icon}
                                                    </span>
                                                )}
                                                <span className="branched-menu__label">{kid.label}</span>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                )
            })}
        </nav>
    )
}