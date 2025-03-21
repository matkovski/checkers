import {useContext, useRef} from 'react';

import {UserContext} from '../services/auth';
import {Move, Movement} from '../models/move';

export default function Board({ moving, game, onMove }) {
    let user = useContext(UserContext);
    let root = useRef(null);
    let another = useRef(null);

    let board = game.board;
    if (game.black === user?.login) {
        board = board.reverse().map(r => r.reverse());
    }

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
                let attempt = new Move([
                    new Movement(game.pieceAt(sx, sy), sx, sy, lx, ly)
                ]);
                if (game.possibleMoves.some(m => m.equals(attempt))) {
                    let cell = root.current.querySelector('[data-x="' + lx + '"][data-y="' + ly + '"]');
                    cell.appendChild(span);
                    onMove && onMove(attempt);
                }
            }

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

    return (
        <div className="board" ref={root}>
            {board.map((row, y) => (
                <div>
                    {row.map((piece, x) => (
                        <span data-x={x} data-y={y} className={(x + y) % 2 ? 'odd' : 'even'}>
                            {piece === '-' || <span data-piece={piece} onMouseDown={mouseDown}></span>}
                        </span>
                    ))}
                </div>
            ))}
            <div ref={another} style={{position:'fixed',width:'4px',height:'4px',background:'red',transform:'translate(-2px,-2px)',left:'0',top:'0',zIndex:'1000'}}></div>
        </div>
    )
}