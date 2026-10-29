export type Token = {access_token: string; token_type: string}

export type User = {
    id: string,
    email: string,
    full_name: string,
    created_at: string,
    updated_at: string
}

export type LoginInput = {email: string, password: string}
export type RegisterInput = LoginInput & {full_name?: string}

export interface CategoryExpense {
    category_id: string
    category_name: string
    total: string
}

export interface MonthlyBalance {
    year: number
    month: number
    total_income: string
    total_expenses: string
    balance: string
    expenses_by_category: CategoryExpense[]
}

export const MOVEMENT_TYPES = ['COMPRA', 'TRANSFERENCIA', 'RETIRO', 'PAGO', 'OTRO'] as const
export type MovementType = (typeof MOVEMENT_TYPES)[number]

export interface Category {
    id: string
    name: string
    user_id: string | null
    is_global: boolean
    created_at: string
    updated_at: string
}

export interface Movement {
    id: string
    user_id: string
    category_id: string
    movement_type: MovementType
    amount: string
    description: string | null
    movement_date: string
    created_at: string
    updated_at: string
}

export interface MovementCreateInput {
    category_id: string
    movement_type: MovementType
    amount: string
    description?: string
    movement_date?: string
}

export interface MovementUpdateInput {
    category_id?: string
    movement_type?: MovementType
    amount?: string
    description?: string | null
    movement_date?: string
}

export const INCOME_SOURCE = ['SALARIO', 'FREELANCE', 'CONSIGNACIONES', 'OTROS'] as const
export type IncomeSource = (typeof INCOME_SOURCE)[number]

export interface Income {
    id: string
    user_id: string
    source: IncomeSource
    year: number
    month: number
    amount: string
    description: string
    created_at: string
    updated_at: string
}

export interface IncomeCreateInput{
    amount: string
    description?: string | null
    month: number
    year: number
    source: IncomeSource
}

export interface IncomeUpdateInput {
    amount?: string
    description?: string | null
    month?: number
    year?: number
    source?: IncomeSource
}

export interface CategoryInput {
    name: string
}