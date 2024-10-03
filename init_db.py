from sqlalchemy.sql.ddl import DropTable, CreateTable
import aiopg.sa

import db
from settings import config


DB_URL_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = DB_URL_FORMAT.format(**config['postgres'])


async def create_table(engine):
    async with engine.acquire() as connection:
        await connection.execute(DropTable(db.users, if_exists=True))
        await connection.execute(CreateTable(db.users))


async def populate_table(engine):
    async with engine.acquire() as connection:
        await connection.execute(db.users.insert().values(nickname='Johny11', banned=False))
        await connection.execute(db.users.insert().values(nickname='Sh00ter', banned=True))
        await connection.execute(db.users.insert().values(nickname='StAr', banned=False))


async def init_db(app):
    app['db'] = await aiopg.sa.create_engine(db_url)

    await create_table(app['db'])
    await populate_table(app['db'])

    yield

    app['db'].close()
    await app['db'].wait_closed()