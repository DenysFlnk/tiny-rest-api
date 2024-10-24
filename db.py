import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from user_model import User, Base

LOGGER = logging.getLogger('tiny_rest_api_logger')


class Database:
    def __init__(self, url):
        self.connection_url = url
        self.engine = create_engine(self.connection_url)
        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def get_all_users(self) -> list[User]:
        try:
            return self.session.query(User).all()
        except IntegrityError as e:
            LOGGER.warning('Error while getting all users', exc_info=True)
            raise e

    def get_user(self, user_id) -> User:
        try:
            return self.session.query(User).filter_by(id=user_id).one()
        except IntegrityError as e:
            LOGGER.warning(f'Error while getting user with id:{user_id}', exc_info=True)
            raise e

    def add_user(self, user) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError as e:
            LOGGER.warning(f'Error while saving user:{user.id},{user.nickname},{user.is_banned}', exc_info=True)
            self.session.rollback()
            raise e

    def delete_user(self, user_id) -> None:
        try:
            user = self.session.query(User).filter_by(id=user_id).one()
            self.session.delete(user)
            self.session.commit()
        except IntegrityError as e:
            LOGGER.warning(f'Error while deleting user with id:{user_id}', exc_info=True)
            self.session.rollback()
            raise e

    def update_user(self, user_id, user) -> None:
        try:
            old_user = self.session.query(User).filter_by(id=user_id).one()
            old_user.nickname = user.nickname
            old_user.is_banned = user.is_banned

            self.session.commit()
        except IntegrityError as e:
            LOGGER.warning(f'Error while updating user with id:{user_id}', exc_info=True)
            self.session.rollback()
            raise e
