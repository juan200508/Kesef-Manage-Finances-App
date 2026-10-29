import { createBrowserRouter } from 'react-router-dom'
import { AppShell } from './AppShell'
import { ProtectedRoute } from './ProtectedRoute'
import { PublicLayout } from './PublicLayout'
import { RouteErrorPage } from './RouteErrorPage'
import { LoginPage } from '../features/auth/LoginPage'
import { RegisterPage } from '../features/auth/RegisterPage'
import { CategoriesPage } from '../pages/CategoriesPage'
import { DashboardPage } from '../pages/DashBoardPage'
import { IncomesPage } from '../pages/IncomesPage'
import { MovementsPage } from '../pages/MovementsPage'
import { NotFoundPage } from '../pages/NotFoundPage'

export const router = createBrowserRouter([
    {
        // Ruta sin path: cualquier error de render de sus hijas cae en RouteErrorPage
        errorElement: <RouteErrorPage />,
        children: [
            {
                element: <PublicLayout />,
                children: [
                    { path: '/login', element: <LoginPage /> },
                    { path: '/register', element: <RegisterPage /> },
                    { path: '*', element: <NotFoundPage /> },
                ],
            },
            {
                element: <ProtectedRoute />,
                children: [
                    {
                        element: <AppShell />,
                        children: [
                            { path: '/', element: <DashboardPage /> },
                            { path: '/movements', element: <MovementsPage /> },
                            { path: '/incomes', element: <IncomesPage /> },
                            { path: '/categories', element: <CategoriesPage /> },
                        ],
                    },
                ],
            },
        ],
    },
])