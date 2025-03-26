import asyncio
import requests
from sseclient import SSEClient
from json import loads, dumps

from models.game import Game
from models.move import Move
from models.position import Position

root = 'http://localhost:8000/api'
user = {
    'login': 'robot',
    'pwd': 'robot',
}

async def login():
    rq = requests.post(url = root + '/auth/login', json = user, headers = {'Content-type': 'application/json'})
    print(f'Log in {rq}')
    rs = rq.json()
    if 'errors' in rs or 'detail' in rs:
        rq = requests.post(root + '/auth/register', json = user, headers = {'Content-type': 'application/json'})
        rs = rq.json()

        if 'errors' in rs or 'detail' in rs:
            print('I cannot even register, sorry')
            print(rs)
            return
        
        rq = requests.get(url = root + '/auth/confirm?code=' + rs)
        rs = rq.json()
        if 'errors' in rs or 'detail' in rs:
            print('Registered but could not confirm')
            print(rs)
            return
        
        rq = requests.post(url = root + '/auth/login', json = user, headers = {'Content-type': 'application/json'})
        rs = rq.json()
        if 'errors' in rs or 'detail' in rs:
            print('I registered, but did not login, dunno')
            print(rs)
            return

    return rs
        
async def play(token):
    sub = SSEClient(root + '/game/events?token=' + token)
    game = None
    color = None

    for msg in sub:
        data = loads(msg.data)
        if msg.event == 'game':
            children = [p['move'] for p in data['positions'] if p['move']]
            position = Position.start()

            positions = []
            for pos in children:
                if pos:
                    position = position.makemove(Move(**pos))
                positions.append(position)
            
            game = Game(
                id = data['id'],
                white = data['white'] or '',
                black = data['black'] or '',
                positions = positions,
                fen = ''
            )
        
            color = 'w' if data['white'] == 'robot' else 'b'

            print(f'Joined game #{data["id"]} ({(data["white"] + " vs " + data["black"]) if data["white"] and data["black"] else "opponent missing"}) as {"white" if color == "w" else "black"}')
        elif msg.event == 'move':
            if not game:
                print('Incoming move but not game')
                return
            game = game.makemove(Move.parse(data))

        if game.turn == color:
            children = game.position.children()
            if not children:
                print('I lost, bye')
                return
            
            move = None
            value = -10000 if color == 'w' else 10000
            bottoms = []
            tops = []
            for pos in children:
                bottoms.append(pos.bottom2)
                tops.append(pos.top2)
                value2 = pos.top2 if color == 'b' else pos.bottom2
                if color == 'b' and value2 < value or color == 'w' and value2 > value:
                    value = value2
                    move = pos.move
            
            print(f'Moving {move} with value {value}')
            print(f'bottoms are {bottoms}')
            print(f'tops are {tops}')

            rq = requests.post(url = root + '/game/move', json = loads(dumps(move, default=vars)), headers = {'Content-type': 'application/json', 'X-Token': token})
            rs = rq.json()
            if 'error' in rs or 'detail' in rs:
                print('Error while moving')
                print(rs)
                return
        else:
            moves = game.position.possiblemoves()
            if not moves:
                print('I won, bye')
                return


async def main():
    print("Robot started")
    token = await login()
    if token:
        await play(token)

if __name__ == '__main__':
    asyncio.run(main())