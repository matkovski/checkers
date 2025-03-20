import {useContext} from 'react';

import {UserContext} from '../services/auth';

export default function Board({ moving, game }) {
    let user = useContext(UserContext);

    let board = game.board;
    if (game.black === user?.login) {
        board = board.reverse().map(r => r.reverse());
    }

    return (
        <div className="board">
            {board.map((row, y) => (
                <div>
                    {row.map((piece, x) => (
                        <span data-x={x} data-y={y} className={(x + y) % 2 ? 'odd' : 'even'}>
                            {piece === '-' || <span data-piece={piece}></span>}
                        </span>
                    ))}
                </div>
            ))}
        </div>
    )
}