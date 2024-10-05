from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user_model import User


class Database:
    def __init__(self, url):
        self.connection_url = url
        self.engine = create_engine(self.connection_url)
        self.session = sessionmaker(bind=self.engine, autoflush=False, autocommit=True)


    def get_all_users(self):
        session = self.session()
        try:
            return session.query(User).all()
        finally:
            session.close()


    def get_user(self, user_id):
        session = self.session()
        try:
            return session.query(User).filter_by(id=user_id).one()
        finally:
            session.close()


    def add_user(self, user):
        session = self.session()
        try:
            session.query(User).add_entity(user)
        finally:
            session.close()


    def delete_user(self, user_id):
        session = self.session()
        try:
            session.query(User).filter_by(id=user_id).delete()
        finally:
            session.close()


    def update_user(self, user_id, user):
        session = self.session()
        try:
            old_user = session.query(User).filter_by(id=user_id).one()
            old_user.nickname = user.nickname
            old_user.is_banned = user.is_banned
            session.query(User).filter_by(id=user_id).update(old_user)
        finally:
            session.close()