import {useState, useContext, useRef} from 'react';

import {games} from '../services/games';
import {UserContext} from '../services/auth';
import Board from './Board';

export default function Game({ game }) {
    let user = useContext(UserContext);
    let brd = useRef(null);

    if (!game) {
        return (
            <>
                There's no game, why call me
            </>
        )
    }

    let gameOn = game.white && game.black;
    let userToMove = game.turn === 'w' ? game.white : game.black;
    let mymove = user.login === userToMove;

    async function makeMove(move) {
        let ok = await games.makeMove(move);
        // if (!ok) {
        //     brd.current.reset();
        // }
    }

    return (
        <>
            <Board ref={brd} moving={gameOn ? mymove : false} game={game} onMove={makeMove}/>
            {gameOn ? (
                <div className="players">
                    <span className="white">{game.white}</span>
                    vs
                    <span className="black">{game.black}</span>
                </div>
            ) : (
                <div className="waiting">
                    Waiting for opponent...
                </div>
            )}
        </>
    )
}