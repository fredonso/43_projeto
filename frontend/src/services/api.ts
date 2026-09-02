import { ApiError } from "./errors";

export async function createUser(username: string, password: string) {
    const response = await fetch('/api/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: username, password: password})
    })

    if (!response.ok) {
        const jsonError = await response.json();
        throw new ApiError(response.status, jsonError.detail);
    }

    return true;
}