import {get, post, event} from '../shared/fetch';

import Game from '../models/game';
import Move from '../models/move';

class Games {
    private game: Game;
    private callbacks: any[] = [];

    public async onUpdate(callback) {
        this.callbacks.push(callback);

        event('/game/events', {
            game: game => {
                window['game'] = this.game = Game.parse(game);
                this.callbacks.forEach(c => c(this.game));
            },
            move: move => {
                if (!this.game) {
                    throw 'MOVE BUT NOT GAME!';
                }
                this.game = this.game.makeMove(Move.parse(move));
                this.callbacks.forEach(c => c(this.game));
            }
        });
    }

    public async makeMove(move) {
        await post('/game/move', move);
    }

    public async restart() {
        await get('/game/restart');
    }
}

export let games = new Games();

