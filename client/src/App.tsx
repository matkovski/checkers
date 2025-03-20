import Auth from './components/Auth';
import GameZone from './components/GameZone';

import './App.css'

export default function() {

    return (
        <>
            <h1>Checkers</h1>
            <Auth>
                <GameZone/>
            </Auth>
        </>
    )
}
