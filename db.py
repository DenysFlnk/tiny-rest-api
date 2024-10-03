from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean


users = Table(
    'users', MetaData(),
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('nickname', String(20), nullable=False),
    Column('banned', Boolean, nullable=False)
)