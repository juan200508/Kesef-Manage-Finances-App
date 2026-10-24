// src/app/PublicLayout.tsx
import { Outlet } from 'react-router-dom'
import { ThemeToggle } from '../components/ui/ThemeToggle'

export function PublicLayout() {
    return (
        <>
            <div className="fixed top-4 right-4 z-50">
                <ThemeToggle />
            </div>
            <Outlet />
        </>
    )
}