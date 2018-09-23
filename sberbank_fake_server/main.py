from logging import getLogger, StreamHandler, DEBUG

from aiohttp import web

from .apps import (
    echo,
    rest,
)


def init_app(config=None):
    app = web.Application()

    # global storage for sb orders
    app['orders'] = {}

    app.add_subapp('/echo/', echo.init_app())
    app.add_subapp('/payment/rest/', rest.init_app())

    log = getLogger('aiohttp.access')
    log.setLevel(DEBUG)
    # log_format = '%a %t "%r" %s %b %Tfsec'
    handler = StreamHandler()
    # handler.setFormatter(log_format)
    log.addHandler(handler)
    return app


async def async_init_app(config=None):
    """ Init app, start point for gunicorn app """

    return init_app(config=config)
