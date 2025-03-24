import {get, post} from '../shared/fetch';

import Game from '../models/game';

class Games {
    private game: Game;
    private callbacks: any[] = [];

    public async pickup() {
        let game = await get('/game/pickup');
        if (!game) {
            console.log('what? no game?')
        }

        return game;
    }

    public async onUpdate(callback) {
        this.callbacks.push(callback);

        if (!this.game) {
            let game = await this.pickup();
            if (game) {
                this.game = Game.parse(game);
                this.callbacks.forEach(c => c(this.game));
            }
        }
    }

    public async makeMove(move) {
        let game = await post('/game/move', move);

        if (game) {
            this.game = Game.parse(game);
            this.callbacks.forEach(c => c(game));
            return true;
        }

        this.callbacks.forEach(c => c(this.game));
        return false;
    }
}

export let games = new Games();

