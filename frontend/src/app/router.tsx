import { createBrowserRouter, Navigate } from 'react-router-dom'
import { AppShell } from './AppShell'
import { ProtectedRoute } from './ProtectedRoute'
import { PublicLayout } from './PublicLayout'
import { LoginPage } from '../features/auth/LoginPage'
import { RegisterPage } from '../features/auth/RegisterPage'
import { DashboardPage } from '../pages/DashBoardPage'
import { MovementsPage } from '../pages/MovementsPage'
import { IncomesPage } from '../pages/IncomesPage'

export const router = createBrowserRouter([
    {
        element: <PublicLayout />,
        children: [
            { path: '/login', element: <LoginPage /> },
            { path: '/register', element: <RegisterPage /> },
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
                ],
            },
        ],
    },
    { path: '*', element: <Navigate to="/" replace /> },
])