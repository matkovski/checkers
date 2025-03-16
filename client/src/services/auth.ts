import {createContext} from 'react';

import {get, post} from '../shared/fetch';

export let UserContext = createContext(null);

class Auth {
    private subscribers: any[] = [];
    private user: any;

    constructor() {

    }

    // TODO a good publisher would be good
    public subscribe(callback) {
        this.subscribers.push(callback);
        callback(this.user);

        if (this.user) {
            callback(this.user);
        } else {
            this.init();
        }

        return () => {
            this.subscribers = this.subscribers.filter(f => f !== callback);
        }
    }

    public async init() {
        this.user = await get('/auth/shake');
        this.subscribers.forEach(f => f(this.user));
    }

    public async login(login, pwd) {
        let token = await post('/auth/login', { login, pwd });
        if (token) {
            localStorage.setItem('xtoken', token);
            await this.init();
            return !!this.user;
        }

        return false;
    }

    public async register(login, pwd) {
        let user = await post('/auth/register', { login, pwd });
        if (user) {
            return user.code;
        }

        return undefined;
    }

    public async confirm(code) {
        let user = await get('/auth/confirm?code=' + code);
        return !!user;
    }
}

export let auth = new Auth();
