from core.app import app
import asyncio
import websockets
from multiprocessing import Pool

class websocket:
    USERS = set()
    message=None
    

    def init(self, var=[]):
        pool = Pool(processes=1)              # Start a worker processes.
        if len(var)==0:
            var=[5678]
        result = pool.apply_async(self.start, var) # Evaluate "f(10)" asynchronously calling callback when finished.


    def start(var=[]):
        start_server = websockets.serve(self.time, 'localhost', var[0])
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    async def time(self,websocket, path):
        import datetime
        import random
        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            await websocket.send(now)
            await asyncio.sleep(random.random() * 3)
        
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
        print('inicio')
        # Register.
        self.USERS.add(websocket)
        producer_task = asyncio.ensure_future( self.producer_handler(websocket, path))
        done, pending = await asyncio.wait([producer_task], return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        
        print('fin')