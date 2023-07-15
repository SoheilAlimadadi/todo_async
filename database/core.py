from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from kernel.settings import DATABASE_URL
from auth.models import User
from tasks.models import Task


async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(DATABASE_URL)

    # Initialize beanie with the Product document class and a database
    await init_beanie(database=client.todo_db, document_models=[User, Task])
