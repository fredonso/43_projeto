import { useAuth } from "../context/AuthContext";

export function Header() {
    const {logout} = useAuth();

    return (
        <header>
            <nav>
                <button onClick={logout} type="button">
                    Sair
                </button>
            </nav>
        </header>
    )
}