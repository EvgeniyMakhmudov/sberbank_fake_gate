from aiohttp import web

from sberbank_fake_server.models import SberbankOrder

from . import checkers


__slots__ = ['init_app']


routes = web.RouteTableDef()


@routes.route('post', '/registerPreAuth.do')
async def handle_registerPreAuth(request):
    request_data = await checkers.registerPreAuth(request)
    sberbank_order = SberbankOrder()
    data = sberbank_order.registerPreAuth(
        orderNumber=request_data['orderNumber'],
        amount=int(request_data['amount']),
        returnUrl=request_data['returnUrl'],
        failUrl=request_data['failUrl'],
        description=request_data['description'],
    )

    request.config_dict['orders'][sberbank_order.id] = sberbank_order
    return web.json_response(data)


@routes.route('post', '/deposit.do')
async def handle_deposit(request):
    request_data = await checkers.deposit(request)

    order = request.config_dict['orders'].get(request_data['orderId'])
    if order is None:
        data = {
            'errorCode': '5',
            'errorMessage': 'Неверный номер заказа',
        }
        return web.json_response(data)

    data = order.deposit(int(request_data['amount']))
    return web.json_response(data)


@routes.route('post', '/reverse.do')
async def handle_reverse(request):
    request_data = await checkers.reverse(request)

    order = request.config_dict['orders'].get(request_data['orderId'])
    if order is None:
        data = {
            'errorCode': '5',
            'errorMessage': 'Неверный номер заказа',
        }
        return web.json_response(data)

    data = order.reverse()
    return web.json_response(data)


@routes.route('post', '/refund.do')
async def handle_refund(request):
    request_data = await checkers.refund(request)

    order = request.config_dict['orders'].get(request_data['orderId'])
    if order is None:
        data = {
            'errorCode': '5',
            'errorMessage': 'Неверный номер заказа',
        }
        return web.json_response(data)

    data = order.refund(int(request_data['amount']))
    return web.json_response(data)


def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app
