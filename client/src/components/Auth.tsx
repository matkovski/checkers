import {useState, useEffect, useRef} from 'react';

import {UserContext, auth} from '../services/auth';
import Login from './Login';

export default function Auth({ children }) {
    let [user, setUser] = useState(null);

    let init = useRef(false);

    useEffect(() => {
        let sub = auth.subscribe(user => {
            init.current = true;
            setUser(user)
        });
        return () => sub();
    }, [])

    return (
        <UserContext value={user}>
            {init.current && (
                <>
                    {user ? children : <Login/>}
                </>
            )}
        </UserContext>
    )
}