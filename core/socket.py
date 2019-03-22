import asyncio
import json
import logging
import websockets


socket_instance = None


class socket:
    USERS = set()
    producer_function=None

    def __init__(self,function):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete( websockets.serve(self.handler, 'localhost', 6789))
        self.loop.run_forever()

    async def notify(self, message):
        if self.USERS:       # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def producer_handler(self, websocket, path):
        while True:
            message = await self.producer_function
            await websocket.send(message)

    async def handler(self, websocket, path):
        # Register.
        self.USERS.add(websocket)
        producer_task = asyncio.ensure_future( self.producer_handler(websocket, path))
        done, pending = await asyncio.wait([producer_task], return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

    def send(self, data):
        return data

    @staticmethod
    def init():
        if socket_instance is None:
            socket_instance = socket()
        return socket_instance
