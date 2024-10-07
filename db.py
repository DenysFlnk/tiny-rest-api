from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user_model import User


class Database:
    def __init__(self, url):
        self.connection_url = url
        self.engine = create_engine(self.connection_url)
        self.session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)


    def get_all_users(self) -> list[User]:
        session = self.session()
        try:
            return session.query(User).all()
        finally:
            session.close()


    def get_user(self, user_id) -> User:
        session = self.session()
        try:
            return session.query(User).filter_by(id=user_id).one()
        finally:
            session.close()


    def add_user(self, user) -> User:
        session = self.session()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()


    def delete_user(self, user_id) -> None:
        session = self.session()
        try:
            session.query(User).filter_by(id=user_id).delete()
            session.commit()
        finally:
            session.close()


    def update_user(self, user_id, user) -> None:
        session = self.session()
        try:
            old_user = session.query(User).filter_by(id=user_id).one()
            old_user.nickname = user.nickname
            old_user.is_banned = user.is_banned

            session.commit()
        finally:
            session.close()