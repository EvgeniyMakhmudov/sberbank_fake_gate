import pytest


@pytest.fixture(scope='function')
def upload(faker):
    return {
        'orderNumber': str(faker.pyint()),
        'amount': str(faker.pyint()),
        'returnUrl': faker.url(),
        'failUrl': 'asd',
        'description': 'qwe asd zxc',
    }


async def test_handle_registerPreAuth(cli, app, upload):
    resp = await cli.post('/payment/rest/registerPreAuth.do', json=upload)
    assert resp.status == 200

    data = await resp.json()
    assert data.get('orderId') is not None
    assert data.get('formUrl') is not None
    assert app['orders'].get(data['orderId']) is not None


async def test_handle_registerPreAuth__fail_orderNumber(cli, upload):
    upload.pop('orderNumber')
    resp = await cli.post('/payment/rest/registerPreAuth.do', json=upload)
    assert resp.status == 400
    assert 'Incorrect orderNumber' in await resp.text()


async def test_handle_registerPreAuth__fail_amount(cli, upload):
    upload.pop('amount')
    resp = await cli.post('/payment/rest/registerPreAuth.do', json=upload)
    assert resp.status == 400
    assert 'Incorrect amount' in await resp.text()


async def test_handle_deposit(cli, app, upload):
    resp = await cli.post('/payment/rest/registerPreAuth.do', json=upload)
    assert resp.status == 200
    auth_data = await resp.json()

    d_data = {
        'orderId': auth_data['orderId'],
        'amount': upload['amount'],
    }
    resp = await cli.post('/payment/rest/deposit.do', json=d_data)
    assert resp.status == 200

    resp_data = await resp.json()
    assert resp_data['errorCode'] == '0'


async def test_handle_reverse__success(cli, app, upload):
    resp = await cli.post('/payment/rest/registerPreAuth.do', json=upload)
    assert resp.status == 200
    auth_data = await resp.json()

    d_data = {
        'orderId': auth_data['orderId'],
        'amount': upload['amount'],
    }
    resp = await cli.post('/payment/rest/deposit.do', json=d_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data['errorCode'] == '0'

    d_data = {
        'orderId': auth_data['orderId'],
    }
    resp = await cli.post('/payment/rest/reverse.do', json=d_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data['errorCode'] == '0'


async def test_handle_reverse__fail(cli, app, upload):
    resp = await cli.post('/payment/rest/registerPreAuth.do', json=upload)
    assert resp.status == 200
    auth_data = await resp.json()

    d_data = {
        'orderId': auth_data['orderId'],
    }
    resp = await cli.post('/payment/rest/reverse.do', json=d_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data['errorCode'] == '0'

    resp = await cli.post('/payment/rest/reverse.do', json=d_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data['errorCode'] != '0'
    assert resp_data['errorMessage']
