from aiohttp.web import run_app

from .main import init_app

if __name__ == '__main__':
    app = init_app()
    run_app(app, port=8000)

    # or manually run gunicorn like
    # gunicorn sberbank_fake_server.main:init_app --bind localhost:8000 --worker-class aiohttp.GunicornWebWorker --reload --access-logfile - --error-logfile - --log-level DEBUG
