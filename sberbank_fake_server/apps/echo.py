from aiohttp import web

__slots__ = ['init_app']


routes = web.RouteTableDef()


@routes.route('*', '/{tail:.*}')
async def echo(request: web.Request):
    data = {
        'method': str(request.method),
        'url': str(request.rel_url),
        'query': request.query_string,
        'body': await request.text(),
    }
    return web.json_response(data=data)


def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app
