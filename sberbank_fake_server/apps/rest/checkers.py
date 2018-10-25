from aiohttp import web


async def registerPreAuth(request):
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


async def deposit(request):
    result = {}
    json = await request.json()

    result['orderId'] = json.get('orderId')
    if result['orderId'] is None:
        raise web.HTTPBadRequest(text='Incorrect orderId')

    result['amount'] = json.get('amount')
    if result['amount'] is None:
        raise web.HTTPBadRequest(text='Incorrect amount')

    return result


async def reverse(request):
    result = {}
    json = await request.json()

    result['orderId'] = json.get('orderId')
    if result['orderId'] is None:
        raise web.HTTPBadRequest(text='Incorrect orderId')

    return result


async def refund(request):
    result = {}
    json = await request.json()

    result['orderId'] = json.get('orderId')
    if result['orderId'] is None:
        raise web.HTTPBadRequest(text='Incorrect orderId')

    result['amount'] = json.get('amount')
    if result['amount'] is None:
        raise web.HTTPBadRequest(text='Incorrect amount')

    return result


async def getOrderStatusExtended(request):
    result = {}
    json = await request.json()

    result['orderId'] = json.get('orderId')
    if result['orderId'] is None:
        raise web.HTTPBadRequest(text='Incorrect orderId')

    return result
