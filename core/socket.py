import asyncio
import json
import logging
import websockets


def init():
    if socket.socket_instance== None:
        socket.socket_instance = socket()
    
    return socket.socket_instance

class socket:
    USERS = set()
    message=None
    socket_instance = None
    loop=None

    async def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def notify(self, message):
        if self.USERS:       # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def producer_handler(self, websocket, path):
        while True and self.USERS:
            if self.message!=None:
                message=self.message
                self.message=None
                await self.notify(message)


    async def handler(self, websocket, path):
        # Register.
        self.USERS.add(websocket)
        producer_task = asyncio.ensure_future( self.producer_handler(websocket, path))
        done, pending = await asyncio.wait([producer_task], return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()