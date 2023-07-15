import logging

from fastapi import FastAPI

from database.core import init_db


app = FastAPI()
coreLogger = logging.getLogger('core')

@app.on_event('startup')
async def connect_db():
    """
    Connect the database on startup event
    """
    await init_db()
    coreLogger.info("Connected to the database successfully.")
