import {Piece} from './constants';

export class Movement {
    public piece: Piece;
    public srcx: number;
    public srcy: number;
    public dstx: number;
    public dsty: number;
    public take: Piece;

    public static parse(json) {
        return new Movement(json.piece, json.srxs, json.srcy, json.dstx, json.dsty, json.take);
    }

    constructor(piece?: Piece, srcx?: number, srcy?: number, dstx?: number, dsty?: number, take?: Piece) {
        this.piece = piece;
        this.srcx = srcx;
        this.srcy = srcy;
        this.dstx = dstx;
        this.dsty = dsty;
        this.take = take;
    }
}

export default class Move {
    public movements: Movement[] = [];

    public static parse(json) {
        return new Move(json.movements.map(mv => Movement.parse(mv)));
    }

    constructor(movements?: Movement[]) {
        this.movements = movements || []
    }
}