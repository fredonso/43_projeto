import { createBrowserRouter, Outlet } from "react-router-dom";
import { AccountCreate, AccountLogin, Tasks, Timeline, ErrorPage, TestToken } from "./components";

export const router = createBrowserRouter([
    {
        element: <Outlet />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: '/account/create',
                element: <AccountCreate />,
            },
            {
                path: '/account/login',
                element: <AccountLogin />,
            },
            {
                element: <TestToken />,
                children: [
                    {
                        path: '/tasks',
                        element: <Tasks />,
                    },
                    {
                        path: '/',
                        element: <Timeline />,
                    },
                ]
            }
        ]
    }
]);