from logging import getLogger, StreamHandler, DEBUG

from aiohttp import web

from .apps import (
    echo,
)


async def init_app():
    app = web.Application()

    app.add_subapp('/echo/', echo.app)

    log = getLogger('aiohttp.access')
    log.setLevel(DEBUG)
    log_format = '%a %t "%r" %s %b %Tfsec'
    handler = StreamHandler()
    # handler.setFormatter(log_format)
    log.addHandler(handler)

    return app
