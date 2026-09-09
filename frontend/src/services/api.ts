import { ApiError } from "./errors";
import type { Task } from "../components/Tasks";

async function handleResponse<T>(response: Response, logout: () => void): Promise<T | null> {
    if (response.status === 401) {
        logout();
        throw new ApiError(401, 'Sessão expirada. Redirecionando...');
    };
    if (response.status === 204) {
        return null as T;
    };
    if (!response.ok) {
        const jsonError = await response.json();
        throw new ApiError(response.status, jsonError.detail);
    };
    return response.json();
}

export async function createUser(username: string, password: string) {
    const response = await fetch('/api/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: username, password: password})
    });

    return handleResponse<boolean>(response, () => {});
}

export async function createTask(task: Task, token: string, logout: () => void) {
    const response = await fetch('/api/tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(task)
    });

    return handleResponse<Task>(response, logout);
}

export async function listTasks(token: string, logout: () => void) {
    const response = await fetch('/api/tasks/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    return handleResponse<Task[]>(response, logout);
}

export async function deleteTask(taskId: number, token: string, logout: () => void) {
    const response = await fetch(`/api/tasks/${taskId}/`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    return handleResponse<void>(response, logout);
}

export async function updateTask(taskId: number, task: Task, token: string, logout: () => void) {
    const response = await fetch(`/api/tasks/${taskId}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(task)
    });

    return handleResponse<Task>(response, logout);
}