import {games} from '../services/games';
import Board from './Board';

export default function Game({ game }) {
    if (!game) {
        return (
            <>
                There's no game, why call me
            </>
        )
    }

    let gameOn = game.white && game.black;

    function makeMove(move) {
        games.makeMove(move);
    }

    function restart() {
        games.restart();
    }

    return (
        <>
            <Board game={game} onMove={makeMove}/>
            {gameOn ? (
                <>
                    <div className="players">
                        <span className="white">{game.white}</span>
                        vs
                        <span className="black">{game.black}</span>
                    </div>
                    {game.ended ? (
                        <a className="ended" onClick={restart}>
                            Game ended. Click to start another.
                        </a>
                    ) : (
                        <div className="turn">
                            {game.turn === 'w' ? 'White' : 'Black'} to move
                        </div>
                    )}
                </>
            ) : (
                <div className="waiting">
                    Waiting for opponent...
                </div>
            )}
        </>
    )
}