import logging

from fastapi import FastAPI

from database.core import init_db
from auth.api.v1 import (
    authentication_router,
    registration_router
)
from tasks.api.v1 import tasks_router

app = FastAPI()
coreLogger = logging.getLogger('core')

@app.on_event('startup')
async def connect_db():
    """
    Connect the database on startup event
    """
    await init_db()
    coreLogger.info("Connected to the database successfully.")

app.include_router(
    registration_router,
    tags=["Registration"],
    prefix="/v1/auth"
)
app.include_router(
    authentication_router,
    tags=["Authentication"],
    prefix="/v1/auth"
)
app.include_router(
    tasks_router,
    tags=["Tasks"],
    prefix="/v1/tasks"
)
