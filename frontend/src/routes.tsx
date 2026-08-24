import { createBrowserRouter } from "react-router-dom";
import { Account, Tasks, Timeline } from "./components";
import { TestToken } from './components/TestToken';

export const router = createBrowserRouter([
    {
        path: '/account',
        element: <Account />,
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
]);