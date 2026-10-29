import { Link } from 'react-router-dom'
import { Card } from '../components/ui/Card'

export function NotFoundPage() {
    return (
        <main className="mx-auto mt-24 max-w-sm px-4">
            <title>Not found · Kesef</title>
            <Card className="space-y-3 text-center">
                <p className="text-4xl font-semibold text-brand">404</p>
                <p className="text-sm text-content-muted">This page doesn't exist.</p>
                <Link to="/" className="text-sm text-brand">Go to the dashboard</Link>
            </Card>
        </main>
    )
}