from aiohttp import web

from db import Database
from routes import setup_routes
from settings import config

# TODO: change config to ENV
DB_URL_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = DB_URL_FORMAT.format(**config['postgres'])


def main():
    app = web.Application()

    setup_routes(app)
    init_db(app)

    web.run_app(app)


def init_db(app):
    db = Database(db_url)
    app['db'] = db


if __name__ == '__main__':
    main()