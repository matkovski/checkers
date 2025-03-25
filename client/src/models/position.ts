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
                dirs.forEach(([dx, dy]) => moves.push(...this.getmoves(x, y, dx, dy)));
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
            let x0 = mv.srcx;
            let y0 = mv.srcy;
            let x1 = mv.dstx;
            let y1 = mv.dsty;
            let piece = mv.piece === 'c' && y1 === 7 ? 'q' : (mv.piece === 'C' && y1 === 0 ? 'Q' : mv.piece);
            field[y0][x0] = '-';
            field[y1][x1] = piece;
            if (mv.take) {
                let stepx = Math.sign(x1 - x0);
                let stepy = Math.sign(y1 - y0);
                for (let i = 1; x0 + stepx * i !== x1; i ++) {
                    field[y0 + stepy * i][x0 + stepx * i] = '-';
                }
            }
        });

        let turn: Color = this.turn === 'w' ? 'b' : 'w';

        return new Position(move, turn, field);
    }

    private getmoves(x, y, dx, dy) {
        let moves = []
        if (x + dx < 0 || x + dx > 7 || y + dy < 0 || y + dy > 7) {
            return moves;
        }


        let pc = this.field[y][x];
        let enemies = ['c', 'q'].includes(pc) ? ['C', 'Q'] : ['c', 'q'];
        let friends = ['c', 'q'].includes(pc) ? ['c', 'q'] : ['C', 'Q'];
        if ((pc === 'c' || pc === 'q') && this.turn === 'w' ||
            (pc === 'C' || pc === 'Q') && this.turn === 'b' ||
            (pc === 'c' && dy <= 0 || pc === 'C' && dy >= 0)) {
            return moves;
        }

        if (pc === 'c' || pc === 'C') {
            if (this.field[y + dy][x + dx] === '-') {
                moves.push(new Move([new Movement(pc, x, y, x + dx, y + dy)]));
            }
    
            if (enemies.includes(this.field[y + dy][x + dx]) && this.field[y + dy * 2][x + dx * 2] === '-') {
                moves.push(new Move([new Movement(pc, x, y, x + dx * 2, y + dy * 2, this.field[y + dy][x + dx])]));
            }
        }

        if (pc === 'Q' || pc === 'q') {
            let taken = false;
            for (let i = 1; ; i ++) {
                if (x + dx * i < 0 || x + dx * i > 7 || y + dy * i < 0 || y + dy * i > 7) {
                    break;
                }
                if (friends.includes(this.field[y + dy * i][x + dx * i])) {
                    break;
                }

                if (this.field[y + dy * i][x + dx * i] === '-') {
                    moves.push(new Move([new Movement(pc, x, y, x + dx * 1, y + dy * 1)]));
                }

                if (x + dx * (i + 1) < 0 || x + dx * (i + 1) > 7 || y + dy * (i + 1) < 0 || y + dy * (i + 1) > 7) {
                    break;
                }
                if (!taken && enemies.includes(this.field[y + dy * i][x + dx * i]) && this.field[y + dy * (i + 1)][x + dx * (i + 1)] === '-') {
                    taken = true;
                    moves.push(new Move([new Movement(pc, x, y, x + dx * (i + 1), y + dy * (i + 1), this.field[y + dy * i][x + dx * i])]));
                }
            }
        }

        return moves;
    }
}

