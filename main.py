import logging

import uvicorn
import uvloop
from uvicorn import Server
import asyncio
from asyncio import AbstractEventLoop

from kernel.application import app
from kernel.settings import (
    FAST_HOST,
    FAST_PORT,
    setup_logging
)


coreLogger = logging.getLogger('core')

def get_server(loop: AbstractEventLoop) -> Server:
    """
    takes a event loop and after configuration of the server, returns it.

    Args:
        loop (AbstractEventLoop): asyncio event loop

    Returns:
        Server: uvicorn server
    """
    config = uvicorn.Config(
        app=app,
        host=FAST_HOST,
        port=FAST_PORT,
        loop=loop,
        reload=True
    )
    return Server(config)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    setup_logging()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError as e:
        coreLogger.error(e)
        loop = asyncio.new_event_loop()

    try:
        server = get_server(loop=loop)
        coreLogger.info('Application started, server is running')
        loop.run_until_complete(server.serve())
    finally:
        loop.close()
        coreLogger.info('Application stopped.')
