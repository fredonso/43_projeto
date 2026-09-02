import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { createUser } from "../services/api";

export function AccountCreate() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleFormSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault();
        try {
            if (username.length < 6 || password.length < 6) {
                throw new Error('Usuário e Senha devem ter pelo menos 6 caracteres.')
            }
            await createUser(username, password);
            alert('Conta criada com sucesso!');
            navigate('/account/login', {replace: true, state: {savedUsername: username}});
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
                    Criar conta
                </button>
            </form>
            <Link to='/account/login'>
                Entrar
            </Link>
        </>
    )
}