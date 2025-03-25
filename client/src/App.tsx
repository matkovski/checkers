import Auth from './components/Auth';
import GameZone from './components/GameZone';

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
