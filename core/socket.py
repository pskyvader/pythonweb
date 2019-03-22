import asyncio
import json
import logging
import websockets


socket_instance=None

class socket:
    USERS = set()
    def __init__(self):
        self.loop=asyncio.get_event_loop()
        self.loop.run_until_complete(websockets.serve(self.start, 'localhost', 6789))
        self.loop.run_forever()

    async def notify(self,message):
        if self.USERS:       # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.USERS])



    async def handler(self,websocket, path):
        # Register.
        self.USERS.add(websocket)
        try:
            # Implement logic here.
            await asyncio.wait([user.send("Hello!") for user in self.USERS])
            await asyncio.sleep(10)
        finally:
            # Unregister.
            self.USERS.remove(websocket)


    async def producer_handler(self,websocket, path):
        while True:
            message = await producer()
            await websocket.send(message)

    async def start(self,websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.notify(message)
        finally:
            await self.unregister(websocket)


        producer_task = asyncio.ensure_future( self.producer_handler(websocket, path))
        done, pending = await asyncio.wait( [producer_task], return_when=asyncio.FIRST_COMPLETED)
    
    @staticmethod
    def init():
        if socket_instance is None:
            socket_instance=socket()
        return socket_instance

    @staticmethod
    def send(data):
        instance=socket.init()
        instance.notify(data)


    @staticmethod
    def stop():


    