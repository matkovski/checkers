import {Piece} from './constants';

export class Movement {
    public piece: Piece;
    public srcx: number;
    public srcy: number;
    public dstx: number;
    public dsty: number;
    public take: Piece;

    public static parse(json) {
        return new Movement(json.piece, json.srcx, json.srcy, json.dstx, json.dsty, json.take);
    }

    constructor(piece?: Piece, srcx?: number, srcy?: number, dstx?: number, dsty?: number, take?: Piece) {
        this.piece = piece;
        this.srcx = srcx;
        this.srcy = srcy;
        this.dstx = dstx;
        this.dsty = dsty;
        this.take = take;
    }

    public equals(other: Movement) {
        if (!other) {
            return false;
        }

        return this.piece === other.piece && this.srcx === other.srcx && this.srcy === other.srcy && this.dstx === other.dstx && this.dsty === other.dsty && this.take === other.take;
    }
}

export class Move {
    public movements: Movement[] = [];

    public static parse(json) {
        return new Move(json.movements.map(mv => Movement.parse(mv)));
    }

    constructor(movements?: Movement[]) {
        this.movements = movements || []
    }

    public equals(other: Move) {
        if (!other || other.movements.length !== this.movements.length) {
            return false;
        }

        return this.movements.every((mv, i) => mv.equals(other.movements[i]));
    }
}

export default Move;
