import {get, post, event} from '../shared/fetch';

import Game from '../models/game';

class Games {
    private game: Game;
    private callbacks: any[] = [];

    public async onUpdate(callback) {
        this.callbacks.push(callback);

        event('/game/events', game => {
            window['game'] = this.game = Game.parse(game);
            this.callbacks.forEach(c => c(this.game));
        });
    }

    public async makeMove(move) {
        await post('/game/move', move);
    }
}

export let games = new Games();

