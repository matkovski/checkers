import {useState, useContext} from 'react';

import {UserContext} from '../services/auth';
import Board from './Board';

export default function Game({ game }) {
    let user = useContext(UserContext);

    if (!game) {
        return (
            <>
                There's no game, why call me
            </>
        )
    }

    let gameOn = game.white && game.black;
    let userToMove = game.turn === 'w' ? game.white : game.black;
    let mymove = user.name === userToMove;

    return (
        <>
            <Board moving={gameOn ? mymove : false} game={game}/>
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