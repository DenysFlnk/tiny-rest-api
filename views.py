from aiohttp import web

import db


async def get_all_users(request):
    async with request.app['db'].acquire() as connection:
        cursor = await connection.execute(db.users.select())
        users_list = await cursor.fetchall()

    user_jsons = []
    for user in users_list:
        user_jsons.append(dict(user))

    return web.json_response(user_jsons)


async def get_user(request):
    user_id = request.match_info['user_id']

    async with request.app['db'].acquire() as connection:
        cursor = await connection.execute(db.users.select().where(db.users.c.id == user_id))
        user = await cursor.fetchone()

    user_json = dict(user)
    return web.json_response(user_json)


async def delete_user(request):
    user_id = request.match_info['user_id']

    async with request.app['db'].acquire() as connection:
        await connection.execute(db.users.delete().where(db.users.c.id == user_id))

    return web.Response(status=204)


async def update_user(request):
    user_id = request.match_info['user_id']

    data = await request.json()
    nickname = data.get('nickname')
    banned = data.get('banned')

    async with request.app['db'].acquire() as connection:
        await connection.execute(
            db.users.update().where(db.users.c.id == user_id).values(nickname=nickname, banned=banned)
        )

    return web.Response(status=204)


async def create_user(request):
    data = await request.json()
    nickname = data.get('nickname')
    banned = data.get('banned')

    async with request.app['db'].acquire() as connection:
        result = await connection.execute(
            db.users.insert().values(nickname=nickname, banned=banned).returning(db.users.c.id)
        )
        new_id = await result.scalar()
        cursor = await connection.execute(db.users.select().where(db.users.c.id == new_id))
        user = await cursor.fetchone()

    user_json = dict(user)
    return web.json_response(user_json, status=201)