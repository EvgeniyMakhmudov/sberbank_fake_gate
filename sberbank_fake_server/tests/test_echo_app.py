import json


async def test_echo(cli):
    resp = await cli.post('/echo/test_url', json={'msg': 'test_msg'})
    assert resp.status == 200

    data = await resp.json()
    assert data['method'] == 'POST'
    assert data['url'] == '/echo/test_url'
    assert json.loads(data['body'])['msg'] == 'test_msg'
