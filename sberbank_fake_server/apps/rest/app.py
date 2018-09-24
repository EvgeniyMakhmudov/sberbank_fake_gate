from aiohttp import web

from sberbank_fake_server.models import SberbankOrder


__slots__ = ['init_app']


routes = web.RouteTableDef()


async def check_and_return(request):
    result = {}
    json = await request.json()

    result['orderNumber'] = json.get('orderNumber')
    if result['orderNumber'] is None:
        raise web.HTTPBadRequest(text='Incorrect orderNumber')

    result['amount'] = json.get('amount')
    if result['amount'] is None:
        raise web.HTTPBadRequest(text='Incorrect amount')

    result['returnUrl'] = json.get('returnUrl')
    result['failUrl'] = json.get('failUrl')
    result['description'] = json.get('description')

    return result


@routes.route('post', '/registerPreAuth.do')
async def handle_registerPreAuth(request):
    request_data = await check_and_return(request)
    sberbank_order = SberbankOrder()
    data = sberbank_order.registerPreAuth(
        orderNumber=request_data['orderNumber'],
        amount=request_data['amount'],
        returnUrl=request_data['returnUrl'],
        failUrl=request_data['failUrl'],
        description=request_data['description'],
    )

    request.config_dict['orders'][sberbank_order.id] = sberbank_order
    return web.json_response(data)


def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app
