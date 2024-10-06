from http import HTTPStatus

from aiohttp import web

from user_model import User


def get_all_users(request):
    db = request.app['db']

    all_users = db.get_all_users()
    all_users_dict = [user_to_dict(user) for user in all_users]

    return web.json_response(all_users_dict, status=HTTPStatus.OK)


async def get_user(request):
    db = request.app['db']
    user_id = request.match_info['user_id']

    user = db.get_user(user_id)

    return web.json_response(user_to_dict(user), status=HTTPStatus.OK)


def delete_user(request):
    db = request.app['db']
    user_id = request.match_info['user_id']

    db.delete_user(user_id)

    return web.HTTPNoContent()


async def update_user(request):
    db = request.app['db']
    data = await request.json()

    user = User()
    user.id = request.match_info['user_id']
    user.nickname = data.get('nickname')
    user.is_banned = data.get('is_banned')

    db.update_user(user.id, user)

    return web.HTTPNoContent()


async def create_user(request):
    db = request.app['db']
    data = await request.json()

    user = User()
    user.nickname = data.get('nickname')
    user.is_banned = data.get('is_banned')

    created_user = db.add_user(user)

    return web.json_response(user_to_dict(created_user), status=HTTPStatus.CREATED)


def user_to_dict(user):
    return {
        "id": user.id,
        "nickname": user.nickname,
        "is_banned": user.is_banned
    }