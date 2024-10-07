import logging
import os

from aiohttp import web

from db import Database
import user_service


ROOT_URL = '/users'
USER_URL = '/users/{user_id}'


def main():
    app = web.Application()

    init_db(app)
    init_api(app)
    setup_logger()

    web.run_app(app, port=os.environ.get('APP_PORT', 8080))


def init_db(app):
    db_name = os.environ.get('DATABASE_NAME', 'tiny_rest_api')
    db_user = os.environ.get('POSTGRES_USER', 'postgres')
    db_password = os.environ.get('POSTGRES_PASSWORD', 'userPassword')
    db_host = os.environ.get('POSTGRES_HOST', 'localhost')
    db_port = os.environ.get('POSTGRES_PORT', '5432')

    db = Database(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    app['db'] = db


def init_api(app):
    app.router.add_get(ROOT_URL, user_service.get_all_users)
    app.router.add_get(USER_URL, user_service.get_user)
    app.router.add_delete(USER_URL, user_service.delete_user)
    app.router.add_put(USER_URL, user_service.update_user)
    app.router.add_post(ROOT_URL, user_service.create_user)


def setup_logger():
    logger = logging.getLogger('tiny_rest_api_logger')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(name)s] - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('tiny_rest_api_logger.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


if __name__ == '__main__':
    main()