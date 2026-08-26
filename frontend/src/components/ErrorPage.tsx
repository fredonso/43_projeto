import { isRouteErrorResponse, Link, useRouteError } from "react-router-dom";

export function ErrorPage() {
    const error = useRouteError();
    let pageError: string

    if (isRouteErrorResponse(error)) {
        pageError = error.statusText || error.data?.message || 'Erro de rota'
    } else if (error instanceof Error) {
        pageError = error.message
    } else if (typeof error === 'string') {
        pageError = error
    } else  {
        pageError = 'Ocorreu um erro desconhecido'
    }

    return (
        <div>
            <h1>Oops! Página não encontrada ou erro interno.</h1>
            <p>{pageError}</p>
            <Link to='/'>
                Voltar para a Página Inicial
            </Link>
        </div>
    )
}