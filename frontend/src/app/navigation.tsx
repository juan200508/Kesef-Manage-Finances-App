import type { MenuItem } from '../components/ui/BranchedMenu'
import { RepeatIcon, TrendingUpIcon, TagIcon } from '../components/ui/icons'

export const NAV_ITEMS: MenuItem[] = [
    { value: '/', label: 'Dashboard' },
    {
        label: 'Money',
        children: [
            { value: '/movements', label: 'Movements', icon: <RepeatIcon /> },
            { value: '/incomes', label: 'Incomes', icon: <TrendingUpIcon /> },
        ],
    },
    { 
        label: 'Manage', 
        children: [
            { value: '/categories', label: 'Categories', icon: <TagIcon /> }
        ] 
    },
]