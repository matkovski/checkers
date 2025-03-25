import {Piece, Color} from './constants';
import {Move, Movement} from './move';

let dirs = [[-1, -1], [-1, 1], [1, -1], [1, 1]];

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
        let moves = [];
        this.field.forEach((row, y) => {
            row.forEach((pc, x) => {
                if (pc === '-') {
                    return;
                }
                dirs.forEach(([dx, dy]) => moves.push(...this.getmoves(this.field, x, y, dx, dy)));
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

    private getmoves(field, x, y, dx, dy, onlyTakeBy = undefined) {
        let moves = []
        if (x + dx < 0 || x + dx > 7 || y + dy < 0 || y + dy > 7) {
            return moves;
        }

        let pc = onlyTakeBy || field[y][x];
        let enemies = ['c', 'q'].includes(pc) ? ['C', 'Q'] : ['c', 'q'];
        let friends = ['c', 'q'].includes(pc) ? ['c', 'q'] : ['C', 'Q'];
        if ((pc === 'c' || pc === 'q') && this.turn === 'w' ||
            (pc === 'C' || pc === 'Q') && this.turn === 'b' ||
            (pc === 'c' && dy <= 0 || pc === 'C' && dy >= 0)) {
            return moves;
        }

        if (pc === 'c' || pc === 'C') {
            if (!onlyTakeBy) {
                if (field[y + dy][x + dx] === '-') {
                    moves.push(new Move([new Movement(pc, x, y, x + dx, y + dy)]));
                }
            }
    
            if (x + dx * 2 >= 0 && x + dx * 2 <= 7 && y + dy * 2 >= 0 && y + dy * 2 <= 7) {
                if (enemies.includes(field[y + dy][x + dx]) && field[y + dy * 2][x + dx * 2] === '-') {
                    let move = new Move([new Movement(pc, x, y, x + dx * 2, y + dy * 2, field[y + dy][x + dx])]);
                    moves.push(move);

                    let field2 = field.map(r => r.slice());
                    field2[y + dx][x + dx] = '-';

                    dirs.forEach(([ddx, ddy]) => {
                        this.getmoves(field2, x + dx * 2, y + dy * 2, ddx, ddy, pc).forEach(e => {
                            let cont = new Move([
                                ...move.movements,
                                ...e.movements,
                            ]);
                            moves.push(cont);
                        })
                    }, []);
                }
            }
        }

        if (pc === 'Q' || pc === 'q') {
            let taken = false;
            for (let i = 1; ; i ++) {
                if (x + dx * i < 0 || x + dx * i > 7 || y + dy * i < 0 || y + dy * i > 7) {
                    break;
                }
                if (friends.includes(field[y + dy * i][x + dx * i])) {
                    break;
                }

                if (!onlyTakeBy) {
                    if (field[y + dy * i][x + dx * i] === '-') {
                        if (!onlyTakeBy || taken) {
                            moves.push(new Move([new Movement(pc, x, y, x + dx * i, y + dy * i)]));
                        }
                    }
                }

                if (x + dx * (i + 1) < 0 || x + dx * (i + 1) > 7 || y + dy * (i + 1) < 0 || y + dy * (i + 1) > 7) {
                    break;
                }
                if (!taken && enemies.includes(field[y + dy * i][x + dx * i]) && field[y + dy * (i + 1)][x + dx * (i + 1)] === '-') {
                    taken = true;
                    let move = new Move([new Movement(pc, x, y, x + dx * (i + 1), y + dy * (i + 1), field[y + dy * i][x + dx * i])]);
                    moves.push(move);

                    let field2 = field.map(r => r.slice());
                    field2[y + dy * i][x + dx * i] = '-';

                    dirs.forEach(([ddx, ddy]) => {
                        this.getmoves(field2, x + dx * (i + 1), y + dy * (i + 1), ddx, ddy, pc).forEach(e => {
                            let cont = new Move([
                                ...move.movements,
                                ...e.movements,
                            ]);
                            moves.push(cont);
                        })
                    }, []);
                }
            }
        }

        return moves;
    }
}

