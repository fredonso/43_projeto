import { createContext, useState, useContext, useEffect } from "react";
import type { ReactNode } from "react";
import { ApiError } from '../services/errors';

interface AuthContextInterface {
    token: string | null,
    login: (username: string, password: string) => Promise<void>,
    logout: () => void
}

export const AuthContext = createContext<AuthContextInterface | null>(null)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = useState(() => {
        const savedToken = localStorage.getItem('Stoken');
        return savedToken ? JSON.parse(savedToken) : null;
    });

    useEffect(() => {
        if (token === null) {
            localStorage.removeItem('Stoken');
        } else {
            localStorage.setItem('Stoken', JSON.stringify(token));
        }
    }, [token]);

    const login = async (username: string, password: string) => {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username: username, password: password})
        });

        if (!response.ok) {
            const jsonError = await response.json();
            throw new ApiError(response.status, jsonError.detail);
        }

        const data = await response.json();

        setToken(data['access_token']);
    };

    const logout = () => {
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error('useAuth fora de posição.')
    }

    return context;
}