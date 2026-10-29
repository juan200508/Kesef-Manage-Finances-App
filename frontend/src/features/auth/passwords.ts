export const PASSWORD_MAX = 72

export const PASSWORD_RULES = [
  { id: 'length', label: 'At least 8 characters', test: (v: string) => v.length >= 8 },
  { id: 'number', label: 'At least one number', test: (v: string) => /[0-9]/.test(v) },
  { id: 'special', label: 'At least one special character', test: (v: string) => /[^A-Za-z0-9\s]/.test(v) },
] as const

export function validatePassword(value: string): true | string {
  const failed = PASSWORD_RULES.find((rule) => !rule.test(value))
  return failed ? failed.label : true
}