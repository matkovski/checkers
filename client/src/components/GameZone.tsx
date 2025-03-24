import {useState, useEffect} from 'react';

import Game from './Game';
import {games} from '../services/games';

export default function GameZone() {
    let [game, setGame] = useState(undefined);

    useEffect(() => {
        games.onUpdate(game => {
            setGame(game);
        })
    }, [])

    return (
        <>
            {game ? (
                <Game game={game}/>
            ) : (
                <>
                Game is not running. This should never appear.
                </>
            )}
        </>
    )
}
