from sqlalchemy.orm import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_all(self):
        return self._db_session.query(User).all()

    def get_limit(self, limit, offset):
        return self._db_session.query(User).limit(limit).offset(offset).all()

    def get_by_id(self, uid):
        return self._db_session.query(User).filter(User.id == uid).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def create(self, data):
        obj = User(**data)
        self._db_session.add(obj)
        self._db_session.commit()
        return obj

    def update(self, data):
        obj = self.get_by_id(data.get('id'))
        if obj:
            if data.get('name'):
                obj.name = data.get('name')
            if data.get('surname'):
                obj.surname = data.get('surname')
            if data.get('favorite_genre'):
                obj.favorite_genre = data.get('favorite_genre')
            if data.get('password'):
                obj.password = data.get('password')
            self._db_session.add(obj)
            self._db_session.commit()
            return obj
        return None
