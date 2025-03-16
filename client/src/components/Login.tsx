import {useState} from 'react'

import {auth} from '../services/auth';

export default function() {
    let [login, setLogin] = useState('');
    let [pwd, setPwd] = useState('');
    let [code, setCode] = useState('');
    let [error, setError] = useState(false);
    let [confirmed, setConfirmed] = useState(false);

    async function signin(e) {
        e.preventDefault();
        let ok = await auth.login(login, pwd);
        if (ok === error) {
            setError(!ok);
        }
    }

    async function register(e) {
        e.preventDefault();

        let inCode = await auth.register(login, pwd);
        if (inCode) {
            setCode(inCode);
        } else {
            setError(true);
        }
    }

    async function confirm() {
        let ok = await auth.confirm(code);
        setConfirmed(ok);
        setCode('');
    }

    function resetError() {
        error && setError(false);
        confirmed && setConfirmed(false);
    }

    return (
        <form className="login">
            <input type="text" name="login" value={login} onChange={e => setLogin(e.target.value)} placeholder="Login" onInput={resetError}/>
            <input type="password" name="pwd" value={pwd} onChange={e => setPwd(e.target.value)} placeholder="Password" onInput={resetError}/>
            <button onClick={signin}>Sign in</button>
            <button onClick={register}>Register</button>
            {error && (
                <label>Please try again</label>
            )}
            {code && (
                <label><a onClick={confirm}>Click to confirm: {code}</a></label>
            )}
            {confirmed && (
                <label>Confirmed, now sign in</label>
            )}
        </form>
    )
}