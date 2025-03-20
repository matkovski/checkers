import Position from './position';
import Move from './move';

export default class Game {
    public white: string;
    public black: string;
    public positions: Position[] = [];

    static parse(json) {
        try {
            // debugger;
            return new Game(json.white, json.black, json.positons?.map(pos => Position.parse(pos)) || []);
        } catch {
            return new Game();
        }
    }

    public get board() {
        let pos = this.positions[this.positions.length - 1];
        return pos?.board || [];
    }

    constructor(white?: string, black?: string, positions?: Position[]) {
        this.white = white || undefined;
        this.black = black || undefined;
        this.positions = positions?.length ? positions : [Position.start()];
        this.refreshFen();
    }

    public get turn() {
        let position = this.positions[this.positions.length - 1];
        return position?.turn || undefined;
    }

    public get ended() {
        let position = this.positions[this.positions.length - 1];

        return position?.children || true;
    }

    public makeMove(moves: Move[]) {

    }

    private refreshFen() {
        // pos = self.positions[-1]

        // if not pos:
        //     self.fen = '--------------------------------/w'

        // field = pos.board()
        // self.fen = ''
        // for y in range(8):
        //     for x in range(8):
        //         if (x + y) % 2 == 0:
        // continue
        // self.fen += field[y][x]

        // self.fen += '/' + pos.turn
    }
}