import {get, post} from '../shared/fetch';

import Game from '../models/game';

class Games {
    public async pickup() {
        let game = await get('/game/pickup');
        if (!game) {
            console.log('what? no game?')
        }

        return Game.parse(game);
    }
}

export let games = new Games();

