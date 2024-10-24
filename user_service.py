import logging
import uuid
from http import HTTPStatus

from aiohttp import web
from sqlalchemy.exc import NoResultFound, StatementError

from user_model import User

LOGGER = logging.getLogger('tiny_rest_api_logger')

INVALID_VALUES_MESSAGE = 'One or more provided values are invalid'


def get_all_users(request):
    request_id = str(uuid.uuid1())
    LOGGER.info(f'{request} <Request_id:{request_id}> -> get_all_users()')
    db = request.app['db']

    all_users = db.get_all_users()
    all_users_dict = [user_to_dict(user) for user in all_users]

    return web.json_response(all_users_dict, status=HTTPStatus.OK)


def get_user(request):
    request_id = str(uuid.uuid1())
    LOGGER.info(f'{request} <Request_id:{request_id}> -> get_user()')
    db = request.app['db']
    user_id = request.match_info['user_id']

    try:
        user = db.get_user(user_id)
    except NoResultFound:
        LOGGER.warning(f'<Request_id:{request_id}> -> User with id:{user_id} not found', exc_info=True)
        return web.HTTPNotFound(reason=f'User with id:{user_id} not found')

    return web.json_response(user_to_dict(user), status=HTTPStatus.OK)


def delete_user(request):
    request_id = str(uuid.uuid1())
    LOGGER.info(f'{request} <Request_id:{request_id}> -> delete_user()')
    db = request.app['db']
    user_id = request.match_info['user_id']

    try:
        db.delete_user(user_id)
    except NoResultFound:
        LOGGER.warning(f'<Request_id:{request_id}> -> User with id:{user_id} not found', exc_info=True)
        return web.HTTPNotFound(reason=f'User with id:{user_id} not found')

    return web.HTTPNoContent()


async def update_user(request):
    request_id = str(uuid.uuid1())
    LOGGER.info(f'{request} <Request_id:{request_id}> -> update_user()')
    db = request.app['db']
    data = await request.json()

    user = User()
    user.id = request.match_info['user_id']
    user.nickname = data.get('nickname')
    user.is_banned = data.get('is_banned')

    try:
        db.update_user(user.id, user)
    except NoResultFound:
        LOGGER.warning(f'<Request_id:{request_id}> -> User with id:{user.id} not found', exc_info=True)
        return web.HTTPNotFound(text=f"User with id:{user.id} not found")
    except StatementError:
        LOGGER.warning(f'<Request_id:{request_id}> -> {INVALID_VALUES_MESSAGE}', exc_info=True)
        return web.HTTPBadRequest(reason=INVALID_VALUES_MESSAGE)

    return web.HTTPNoContent()


async def create_user(request):
    request_id = str(uuid.uuid1())
    LOGGER.info(f'{request} <Request_id:{request_id}> -> create_user()')
    db = request.app['db']
    data = await request.json()

    user = User()
    user.nickname = data.get('nickname')
    user.is_banned = data.get('is_banned')

    try:
        created_user = db.add_user(user)
    except StatementError:
        LOGGER.warning(f'<Request_id:{request_id}> -> {INVALID_VALUES_MESSAGE}', exc_info=True)
        return web.HTTPBadRequest(reason=INVALID_VALUES_MESSAGE)

    return web.json_response(user_to_dict(created_user), status=HTTPStatus.CREATED)


def user_to_dict(user):
    return {
        "id": user.id,
        "nickname": user.nickname,
        "is_banned": user.is_banned
    }
