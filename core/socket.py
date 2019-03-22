import asyncio
import json
import logging
import websockets

class socket:
    STATE = {'value': 0}
    USERS = set()
    def __init__(self):
        logging.basicConfig()
        
    def state_event(self):
        return json.dumps({'type': 'state', self.STATE})

    def users_event(self):
        return json.dumps({'type': 'users', 'count': len(self.USERS)})

    async def notify_state(self):
        if self.USERS:       # asyncio.wait doesn't accept an empty list
            message = state_event()
            await asyncio.wait([user.send(message) for user in USERS])

    async def notify_users(self):
        if USERS:       # asyncio.wait doesn't accept an empty list
            message = users_event()
            await asyncio.wait([user.send(message) for user in USERS])

    async def register(self,websocket):
        USERS.add(websocket)
        await notify_users()

    async def unregister(self,websocket):
        USERS.remove(websocket)
        await notify_users()

    async def counter(self,websocket, path):
        # register(websocket) sends user_event() to websocket
        await register(websocket)
        try:
            await websocket.send(state_event())
            async for message in websocket:
                data = json.loads(message)
                if data['action'] == 'minus':
                    STATE['value'] -= 1
                    await notify_state()
                elif data['action'] == 'plus':
                    STATE['value'] += 1
                    await notify_state()
                else:
                    logging.error(
                        "unsupported event: {}", data)
        finally:
            await unregister(websocket)

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(counter, 'localhost', 6789))
    asyncio.get_event_loop().run_forever()