import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from '../context/AuthContext';
import { Header } from '../components';

export function TestToken() {
    const { token } = useAuth();

    if (!token) {
        return <Navigate to='/account' replace />
    }

    return (
        <>
            <Header />
            <main>
                <Outlet />
            </main>
        </>
    )
}