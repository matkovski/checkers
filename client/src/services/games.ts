import {get, post, event} from '../shared/fetch';

import Game from '../models/game';
import Move from '../models/move';
import Position from '../models/position';

class Games {
    private game: Game;
    private callbacks: any[] = [];

    public async onUpdate(callback) {
        this.callbacks.push(callback);

        event('/game/events', {
            game: game => {
                game = {
                    "id": 1,
                    "white": "another",
                    "black": "login",
                    "positions": [{
                        "move": null,
                        "turn": "w",
                        "field": [
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "c", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "c", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                            ["-", "Q", "-", "-", "-", "-", "-", "-"],
                            ["-", "-", "-", "-", "-", "-", "-", "-"],
                        ]
                    }]
                }
                window['game'] = this.game = Game.parse(game);
                this.game.positions = [Position.parse(game.positions[0])];
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

