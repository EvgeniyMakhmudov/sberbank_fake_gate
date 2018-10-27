def getOrderStatusExtended(order):
    result = {}

    result.update(_base(order))
    result.update(_actions(order))
    result.update(_errors(order))

    funcs = (
        _merchantOrderParams,
        _cardAuthInfo,
        _secureAuthInfo,
        _bindingInfo,
        _paymentAmountInfo,
        _bankInfo,
    )
    for func in funcs:
        d = func(order)
        if d is not None:
            result.update(d)

    return result


def _base(order):
    return {
        'orderNumber': order.orderNumber,
        'currency': getattr(order, 'currency', '643'),
        'orderDescription': getattr(order, 'description', ''),
        'ip': getattr(order, 'ip', ''),
    }


def _actions(order):
    # normal case
    return {
        'actionCode': -100,
        'actionCodeDescription': '',
    }


def _errors(order):
    return {
        'errorCode': '0',
        'errorMessage': 'Успешно',
    }


def _merchantOrderParams(order):
    mop = getattr(order, 'merchantOrderParams', None)
    if mop is None:
        return None
    else:
        return {'merchantOrderParams': mop}


def _cardAuthInfo(order):
    NotImplemented
    return None


def _secureAuthInfo(order):
    NotImplemented
    # because need special access priviligies
    return None


def _bindingInfo(order):
    NotImplemented
    # because need links feature enabled
    return None


def _paymentAmountInfo(order):
    return {
        'approvedAmount': order.approvedAmount,
        'depositedAmount': order.depositedAmount,
        'paymentState': order.status.value,
        'refundedAmount': order.refundedAmount,
    }


def _bankInfo(order):
    # In general it is card info and do not cover by faker gate
    # thats is reason to always return answer like on create order stage
    return {
        'bankCountryCode': 'UNKNOWN',
        'bankCountryName': '<Неизвестно>',
    }
