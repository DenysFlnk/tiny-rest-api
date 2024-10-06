from aiohttp import web

from db import Database
from settings import config
import user_service

# TODO: change config to ENV
DB_URL_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = DB_URL_FORMAT.format(**config['postgres'])

ROOT_URL = '/users'
USER_URL = '/users/{user_id}'


def main():
    app = web.Application()

    init_db(app)
    init_api(app)

    web.run_app(app)


def init_db(app):
    db = Database(db_url)
    app['db'] = db


def init_api(app):
    app.router.add_get(ROOT_URL, user_service.get_all_users)
    app.router.add_get(USER_URL, user_service.get_user)
    app.router.add_delete(USER_URL, user_service.delete_user)
    app.router.add_put(USER_URL, user_service.update_user)
    app.router.add_post(ROOT_URL, user_service.create_user)


if __name__ == '__main__':
    main()