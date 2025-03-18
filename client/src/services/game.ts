import {get, post} from '../shared/fetch';

class Games {
    public async pickup() {
        let game = await get('/game/pickup');
        if (!game) {
            console.log('what? no game?')
        }

        return game;
    }
}

export let games = new Games();

