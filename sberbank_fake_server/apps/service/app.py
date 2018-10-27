import aiohttp
from aiohttp import web


__slots__ = ['init_app']


routes = web.RouteTableDef()


@routes.route('post', '/form_submit')
async def submit(request: web.Request):
    data = await request.json()
    orderId = data['orderId']
    result = data['result']

    if orderId not in request.config_dict['orders']:
        raise web.HTTPBadRequest('OrderId not found')

    sb_order = request.config_dict['orders'][orderId]

    await request.response.write_eof()

    if result == 'success':
        target_url = sb_order.returnUrl
    else:
        target_url = sb_order.failUrl

    async with aiohttp.ClientSession() as session:
        await session.get(target_url)


def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app
