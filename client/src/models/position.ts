import {Piece, Color} from './constants';
import Move from './move';

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
        return []
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
}

