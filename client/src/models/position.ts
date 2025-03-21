import {Piece, Color} from './constants';
import {Move, Movement} from './move';

export default class Position {
    public move: Move;
    public turn: Color = 'w';
    private field: Piece[][] = [];

    public static start() {
        let position = new Position(undefined, 'w', [
            ['-', 'c', '-', 'c', '-', 'c', '-', 'c'],
            ['c', '-', 'c', '-', 'c', '-', 'c', '-'],
            ['-', 'c', '-', 'c', '-', 'c', '-', 'c'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['C', '-', 'C', '-', 'C', '-', 'C', '-'],
            ['-', 'C', '-', 'C', '-', 'C', '-', 'C'],
            ['C', '-', 'C', '-', 'C', '-', 'C', '-'],
        ]);
        return position;
    }

    public static parse(json) {
        return new Position(Move.parse(json.move), json.turn, json.field);
    }

    constructor(move?: Move, turn?: Color, field?: Piece[][]) {
        this.move = move || undefined;
        this.field = field || [];
        this.turn = turn || 'w';
    }

    public get board() {
        return this.field;
    }

    public get children() {
        let dirs = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
        let moves = [];
        this.field.forEach((row, y) => {
            row.forEach((pc, x) => {
                if (pc === '-') {
                    return;
                }
                dirs.forEach(([dx, dy]) => {
                    let can = this.canmove(x, y, dx, dy);
                    can && moves.push(can);
                })
            });
        });
        return moves;
    }

    public pieceAt(x: number, y: number) {
        return this.field[y][x];
    }

    public makeMove(move: Move) {
        // TODO check against children
        
        let field = this.field.map(row => row.slice());
        move.movements.forEach(mv => {
            field[mv.srcy][mv.srcx] = '-';
            field[mv.dsty][mv.dstx] = mv.piece;
            // TODO taking
        });


        let turn: Color = this.turn === 'w' ? 'b' : 'w';

        return new Position(move, turn, field);
    }

    private canmove(x, y, dx, dy) {
        if (x + dx < 0 || x + dx > 7 || y + dy < 0 || y + dy > 7) {
            return;
        }
        let pc = this.field[y][x];
        if ((pc === 'c' || pc === 'q') && this.turn === 'w' ||
            (pc === 'C' || pc === 'Q') && this.turn === 'b' ||
            (pc === 'c' && dy <= 0 || pc === 'C' && dy >= 0)) {
            return;
        }
        if (this.field[y + dy][x + dx] === '-') {
            return new Move([
                new Movement(pc, x, y, x + dx, y + dy)
            ]);
        }
    }
}


function cantake(field, x, y, dx, dy) {

}