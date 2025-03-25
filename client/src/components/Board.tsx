import {useContext, useRef, useState, useEffect} from 'react';

import {UserContext} from '../services/auth';

export default function Board({ game, onMove }) {
    let user = useContext(UserContext);
    let root = useRef(null);
    let [pick, setPick] = useState(null);
    let [rotate] = useState(game.black === user?.login);

    let gameOn = game.white && game.black && game.end === '-';
    let interactive = gameOn && (game.turn === 'w') === (game.white === user.login);
    let board = game.board;
    let span = useRef(null);
    let ignoreClick = useRef(false);
    let bnds = useRef(null);
    let x0 = useRef(undefined);
    let y0 = useRef(undefined);
    let sx = useRef(undefined);
    let sy = useRef(undefined);
    
    if (rotate) {
        board = board.slice().reverse().map(r => r.reverse());
    }

    let possible = pick ? game.possibleMoves.reduce((all, move) => {
        let first = move.movements[0];
        let last = move.movements[move.movements.length - 1];
        if (first.srcx === pick[0] && first.srcy === pick[1]) {
            all.push(last.dstx + '/' + last.dsty);
        }
        return all;
    }, []) : [];

    useEffect(() => {
        document.addEventListener('mousemove', move);
        document.addEventListener('mouseup', up);
        return () => {
            document.removeEventListener('mousemove', move);
            document.removeEventListener('mouseup', up);
        }
    }, []);

    function getxy(ex, ey) {
        if (!bnds.current) {
            return;
        }

        let brd = root.current.getBoundingClientRect();
        let xx = Math.floor((bnds.current.left + bnds.current.width / 2 + ex - x0.current - brd.left) / bnds.current.width);
        let yy = Math.floor((bnds.current.top + bnds.current.height / 2 + ey - y0.current - brd.top) / bnds.current.height);

        if (rotate) {
            xx = 7 - xx;
            yy = 7 - yy;
        }

        return [xx, yy];
    }

    function move(e) {
        if (!span.current) {
            return;
        }

        let x = e.clientX - x0.current;
        let y = e.clientY - y0.current;
        let farEnough = Math.sqrt(x ** 2 + y ** 2) > 10;

        if (!pick && farEnough) {
            setPick([sx.current, sy.current]);
            ignoreClick.current = true;
        }

        span.current.style.left = x + 'px';
        span.current.style.top = y + 'px';
    };

    function up(e) {
        if (!span.current) {
            return;
        }

        if (!ignoreClick.current && !pick) {
            setPick([sx.current, sy.current]);
        } else {
            let [lx, ly] = getxy(e.clientX, e.clientY);
    
            if (lx >= 0 && lx <= 7 && ly >= 0 && lx <= 7) {
                let attempt = game.possibleMoves.find(move => {
                    let fst = move.movements[0];
                    let lst = move.movements[move.movements.length - 1];
                    return fst.srcx === sx.current && fst.srcy === sy.current && lst.dstx === lx && lst.dsty === ly;
                });
                if (attempt) {
                    span.current.style.left = (lx * bnds.current.width) + 'px';
                    span.current.style.top = (ly * bnds.current.height) + 'px';
                    onMove && onMove(attempt);
                }
            }
            setPick(null);
        }

        span.current.style.left = '';
        span.current.style.top = '';

        span.current = undefined;
        bnds.current = undefined;
        sx.current = undefined;
        sy.current = undefined;
        x0.current = undefined;
        y0.current = undefined;
    };


    function mouseDown(event) {
        if (!gameOn || !interactive) {
            return;
        }

        ignoreClick.current = false;

        span.current = event.target;
        if (!span.current.getAttribute('data-piece')) {
            return;
        }

        bnds.current = span.current.getBoundingClientRect();
        x0.current = event.clientX;
        y0.current = event.clientY;
        [sx.current, sy.current] = getxy(x0.current, y0.current);
    }

    function pickTarget(event) {
        if (!gameOn || !pick) {
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
        [sx.current, sy.current] = pick;
        let attempt = game.possibleMoves.find(move => {
            let fst = move.movements[0];
            let lst = move.movements[move.movements.length - 1];
            return fst.srcx === sx.current && fst.srcy === sy.current && lst.dstx === lx && lst.dsty === ly;
        });
        if (attempt) {
            onMove && onMove(attempt);
            setPick(null);
        }
    }

    return (
        <div className={'board' + (interactive ? ' interactive' : '')} ref={root}>
            {board.map((row, y) => (
                <div>
                    {row.map((piece, x) => (
                        <span data-x={rotate ? 7 - x : x} data-y={rotate ? 7 - y : y} className={((x + y) % 2 ? 'odd' : 'even') + (possible.includes((rotate ? 7 - x : x) + '/' + (rotate ? 7 - y : y)) ? ' target' : '')} onClick={pickTarget}>
                            {/* <label>{x}/{y}</label> */}
                            {piece === '-' || <span data-piece={piece} onMouseDown={mouseDown}></span>}
                        </span>
                    ))}
                </div>
            ))}
        </div>
    )
}