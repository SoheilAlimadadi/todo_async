import logging
import uvicorn
from uvicorn import Server
import asyncio
from asyncio import AbstractEventLoop

from kernel.application import app
from kernel.settings import (
    FAST_HOST,
    FAST_PORT,
    setup_logging
)


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
    setup_logging()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError as ex:
        loop = asyncio.new_event_loop()

    try:
        server = get_server(loop=loop)
        loop.run_until_complete(server.serve())
    finally:
        loop.close()
