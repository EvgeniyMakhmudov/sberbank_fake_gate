import pytest

from .main import init_app


@pytest.fixture(scope='function')
def config():
    return None


@pytest.fixture()
def app(config):
    return init_app(config=config)


@pytest.fixture
def cli(loop, aiohttp_client, app):
    return loop.run_until_complete(aiohttp_client(app))
