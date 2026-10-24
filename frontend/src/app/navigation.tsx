import type { MenuItem } from '../components/ui/BranchedMenu'
import { RepeatIcon } from '../components/ui/icons'
// Paso 6: import { TrendingUpIcon } ...   Paso 7: import { TagIcon } ...

export const NAV_ITEMS: MenuItem[] = [
    { value: '/', label: 'Dashboard' },
    {
        label: 'Money',
        children: [
            { value: '/movements', label: 'Movements', icon: <RepeatIcon /> },
            // Paso 6: { value: '/incomes', label: 'Incomes', icon: <TrendingUpIcon /> },
        ],
    },
    // Paso 7:
    // { label: 'Manage', children: [{ value: '/categories', label: 'Categories', icon: <TagIcon /> }] },
]