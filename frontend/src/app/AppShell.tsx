import { useEffect, useState } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { BranchedMenu } from '../components/ui/BranchedMenu'
import { Button } from '../components/ui/Button'
import { CloseIcon, MenuIcon } from '../components/ui/icons'
import { ThemeToggle } from '../components/ui/ThemeToggle'
import { useAuth } from '../features/auth/auth-context'
import { NAV_ITEMS } from './navigation'

export function AppShell() {
    const { signOut } = useAuth()
    const { pathname } = useLocation()
    const navigate = useNavigate()
    const [drawerOpen, setDrawerOpen] = useState(false)

    // Escape cierra el drawer
    useEffect(() => {
        if (!drawerOpen) return
        const onKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Escape') setDrawerOpen(false)
        }
        window.addEventListener('keydown', onKeyDown)
        return () => window.removeEventListener('keydown', onKeyDown)
    }, [drawerOpen])

    const handleSelect = (path: string) => {
        navigate(path)
        setDrawerOpen(false)
    }

    return (
        <div className="min-h-screen">
            {drawerOpen && (
                <div
                    className="fixed inset-0 z-40 bg-black/50"
                    onClick={() => setDrawerOpen(false)}
                />
            )}

            <aside
                className={
                    'fixed inset-y-0 left-0 z-50 w-64 overflow-y-auto border-r border-line bg-surface p-5 transition-transform ' +
                    (drawerOpen ? 'translate-x-0' : '-translate-x-full')
                }
            >
                <div className="mb-6 flex items-center justify-between">
                    <p className="text-lg font-semibold text-brand">Kesef</p>
                    <button
                        type="button"
                        onClick={() => setDrawerOpen(false)}
                        className="cursor-pointer rounded-lg p-1 text-content-muted hover:text-content"
                    >
                        <CloseIcon />
                    </button>
                </div>
                <BranchedMenu items={NAV_ITEMS} active={pathname} onSelect={handleSelect} />
            </aside>

            <header className="flex items-center gap-3 border-b border-line bg-surface px-4 py-3">
                <button
                    type="button"
                    onClick={() => setDrawerOpen(true)}
                    className="cursor-pointer rounded-lg p-2 text-content-muted hover:text-content"
                >
                    <MenuIcon />
                </button>
                <span className="font-semibold text-brand">Kesef</span>

                <div className="ml-auto flex items-center gap-2">
                    <ThemeToggle />
                    <Button variant="ghost" onClick={signOut}>Sign out</Button>
                </div>
            </header>

            <main className="mx-auto max-w-6xl p-6">
                <Outlet />
            </main>
        </div>
    )
}