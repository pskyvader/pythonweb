import asyncio
import json
import logging
import websockets

class socket:
    USERS = set()
    def __init__(self):
        logging.basicConfig()
        

    async def notify_state(self,message):
        if self.USERS:       # asyncio.wait doesn't accept an empty list
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
                await self.notify_state(message)
        finally:
            await self.unregister(websocket)

    loop=asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(counter, 'localhost', 6789))
    loop.run_forever()