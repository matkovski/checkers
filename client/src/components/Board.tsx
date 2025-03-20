export default function Board({ moving, game }) {
    console.log(game);

    let board = game.board;

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