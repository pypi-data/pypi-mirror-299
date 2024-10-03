from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi

import asyncio


# Override the AsyncIOMotorClient class
class Client(AsyncIOMotorClient) :

    main_db: AsyncIOMotorDatabase | None

    # Initialize the client and ping the server
    def __init__(self, uri: str) :
        super().__init__(uri, server_api=ServerApi('1'))
        asyncio.run(self._ping())
        self.main_db = None

    async def _ping(self) :

        # Check if the connection is successful
        try :
            await self.admin.command('ping')
            print('Pinged your deployment. You successfully connected to MongoDB !')

        except Exception as e :
            raise Exception('Could not connect to MongoDB', e)
