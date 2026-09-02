import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { Link, useLocation, useNavigate } from "react-router-dom";

export function AccountLogin() {
    const location = useLocation();
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();

    useEffect(() => {
        if (location.state?.savedUsername) {
            setUsername(location.state.savedUsername);
            navigate(location.pathname, {replace: true, state: {}});
        }
    }, [location, navigate]);

    const handleFormSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault();
        try {
            if (username.length < 6 || password.length < 6) {
                throw new Error('Usuário e Senha devem ter pelo menos 6 caracteres.')
            }
            await login(username, password);
            setUsername('');
            setPassword('');
            alert('Login realizado com sucesso!');
        } catch (erro: any) {
            if (erro.status === 422) {
                alert('Preencha os campos corretamente.');
            } else {
                alert(erro.message);
            }
        }
    }

    return (
        <>
            <form onSubmit={handleFormSubmit}>
                <label>
                    <input 
                    placeholder="Usuário" 
                    type="text" 
                    required 
                    value={username} 
                    onChange={(e) => {setUsername(e.target.value)}}
                    />
                </label>
                <label>
                    <input 
                    placeholder="Senha" 
                    type="password" 
                    required 
                    value={password} 
                    onChange={(e) => {setPassword(e.target.value)}}
                    />
                </label>
                <button type="submit">
                    Login
                </button>
            </form>
            <Link to='/account/create'>
                Criar nova conta
            </Link>
        </>
    )
}