from aiohttp import web

from routes import setup_routes
from init_db import init_db


def main():
    app = web.Application()
    setup_routes(app)
    app.cleanup_ctx.append(init_db)
    web.run_app(app)


if __name__ == '__main__':
    main()