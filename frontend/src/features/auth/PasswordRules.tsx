import { PASSWORD_RULES } from './passwords'

export default function PasswordRules({ value }: { value: string }) {
  return (
    <ul className="mt-2 space-y-1 text-xs" aria-live="polite">
      {PASSWORD_RULES.map((rule) => {
        const ok = rule.test(value)
        return (
          <li key={rule.id} className={ok ? 'text-income' : 'text-content-muted'}>
            <span className="mr-1.5">{ok ? '✓' : '○'}</span>
            {rule.label}
          </li>
        )
      })}
    </ul>
  )
}