import {useContext, useRef, useState} from 'react';

import {UserContext} from '../services/auth';
import {Move, Movement} from '../models/move';

export default function Board({ moving, game, onMove }) {
    let user = useContext(UserContext);
    let root = useRef(null);
    let [pick, setPick] = useState(null);

    let board = game.board;
    let rotate = game.black === user?.login;
    if (rotate) {
        board = board.reverse().map(r => r.reverse());
    }

    let possible = pick ? game.possibleMoves.reduce((all, move) => {
        let first = move.movements[0];
        let last = move.movements[move.movements.length - 1];
        if (first.srcx === pick[0] && first.srcy === pick[1]) {
            all.push(last.dstx + '/' + last.dsty);
        }
        return all;
    }, []) : [];

    let span;
    let piece;

    // TODO multiple movements moves

    function mouseDown(event) {
        span = event.target;
        piece = span.getAttribute('data-piece');
        if (!piece) {
            return;
        }

        let bnds = span.getBoundingClientRect();
        let brd = root.current.getBoundingClientRect();
        let x0 = event.clientX;
        let y0 = event.clientY;
        let [sx, sy] = getxy(x0, y0);

        function getxy(ex, ey) {
            let xx = Math.floor((bnds.left + bnds.width / 2 + ex - x0 - brd.left) / bnds.width);
            let yy = Math.floor((bnds.top + bnds.height / 2 + ey - y0 - brd.top) / bnds.height);

            if (rotate) {
                xx = 7 - xx;
                yy = 7 - yy;
            }

            return [xx, yy];
        }

        function move(e) {
            let x = e.clientX - x0;
            let y = e.clientY - y0;

            span.style.left = x + 'px';
            span.style.top = y + 'px';
        };

        function up(e) {
            let [lx, ly] = getxy(e.clientX, e.clientY);

            if (lx >= 0 && lx <= 7 && ly >= 0 && lx <= 7) {
                let attempt = game.possibleMoves.find(move => {
                    let fst = move.movements[0];
                    let lst = move.movements[move.movements.length - 1];
                    return fst.srcx === sx && fst.srcy === sy && lst.dstx === lx && lst.dsty === ly;
                });
                // if (game.possibleMoves.some(m => m.equals(attempt))) {
                if (attempt) {
                    span.style.left = (lx * bnds.width) + 'px';
                    span.style.top = (ly * bnds.height) + 'px';
                    onMove && onMove(attempt);
                }
            }

            setPick(null);
            span.style.left = '';
            span.style.top = '';

            span = undefined;
            piece = undefined;
            document.removeEventListener('mousemove', move);
            document.removeEventListener('mouseup', up);
        };

        document.addEventListener('mousemove', move);
        document.addEventListener('mouseup', up);
    }

    function pickTarget(event) {
        if (!pick) {
            return;
        }
        let cell = event.target;
        let x = cell.getAttribute('data-x');
        let y = cell.getAttribute('data-y');
        if (!x && !y) {
            return;
        }

        let lx = parseInt(x, 10);
        let ly = parseInt(y, 10);
        let [sx, sy] = pick;
        let attempt = game.possibleMoves.find(move => {
            let fst = move.movements[0];
            let lst = move.movements[move.movements.length - 1];
            return fst.srcx === sx && fst.srcy === sy && lst.dstx === lx && lst.dsty === ly;
        });
        if (attempt) {
            onMove && onMove(attempt);
            setPick(null);
        }
    }

    function pickPiece(event) {
        let piece = event.target;
        if (!piece.getAttribute('data-piece')) {
            return;
        }
        let parent = piece.parentNode;
        let x = parseInt(parent.getAttribute('data-x'), 10);
        let y = parseInt(parent.getAttribute('data-y'), 10);
        if (rotate) {
            x = 7 - x;
            y = 7 - y;
        }
        if (pick && pick[0] === x && pick[1] === y) {
            setPick(null);
        } else {
            setPick([x, y]);
        }
    }

    return (
        <div className="board" ref={root}>
            {board.map((row, y) => (
                <div>
                    {row.map((piece, x) => (
                        <span data-x={rotate ? 7 - x : x} data-y={rotate ? 7 - y : y} className={((x + y) % 2 ? 'odd' : 'even') + (possible.includes(x + '/' + y) ? ' target' : '')} onClick={pickTarget}>
                            {piece === '-' || <span data-piece={piece} onMouseDown={mouseDown} onClick={pickPiece}></span>}
                        </span>
                    ))}
                </div>
            ))}
        </div>
    )
}