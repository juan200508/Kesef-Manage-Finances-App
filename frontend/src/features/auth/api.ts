import { api } from "../../api/client";
import type { LoginInput, RegisterInput, Token, User } from "../../api/types";

export const login = (data: LoginInput) => 
    api.post<Token>('/login', data).then((r) => r.data)

export const register = (data: RegisterInput) => 
    api.post<User>('register', data).then((r) => r.data)