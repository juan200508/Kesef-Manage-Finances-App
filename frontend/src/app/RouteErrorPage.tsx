import { isRouteErrorResponse, useRouteError } from 'react-router-dom'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'

export function RouteErrorPage() {
    const error = useRouteError()
    const detail = isRouteErrorResponse(error) ? `${error.status} ${error.statusText}` : null

    return (
        <main className="mx-auto mt-24 max-w-sm px-4">
            <title>Error · Kesef</title>
            <Card className="space-y-4 text-center">
                <h1 className="text-lg font-semibold">Something went wrong</h1>
                {detail && <p className="text-sm text-content-muted">{detail}</p>}
                <div className="flex justify-center gap-2">
                    <Button onClick={() => window.location.reload()}>Reload</Button>
                    <Button variant="ghost" onClick={() => window.location.assign('/')}>Go home</Button>
                </div>
            </Card>
        </main>
    )
}