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
        return json.dumps({'type': 'state', **self.STATE})

    async def notify_state(self):
        if self.USERS:       # asyncio.wait doesn't accept an empty list
            message = self.state_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self,websocket):
        self.USERS.add(websocket)

    async def unregister(self,websocket):
        self.USERS.remove(websocket)

    




    async def counter(self,websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)
                if data['action'] == 'minus':
                    self.STATE['value'] -= 1
                    await self.notify_state()
                elif data['action'] == 'plus':
                    self.STATE['value'] += 1
                    await self.notify_state()
                else:
                    logging.error( "unsupported event: {}", data)
        finally:
            await self.unregister(websocket)

    loop=asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(counter, 'localhost', 6789))
    loop.run_forever()