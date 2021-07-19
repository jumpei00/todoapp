from datetime import datetime
import logging

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.base import session_scope
from utils.utils import TIME_RE
from utils.utils import TIME_FORMAT

logger = logging.getLogger(__name__)


class DataUpdateError(Exception):
    message = 'try get data, but not it'


class Todo(Base):
    __tablename__ = 'todo'
    timestamp = Column(DateTime, primary_key=True)
    contents = Column(String)
    priority = Column(String)

    @property
    def values(self):
        return {'timestamp': self.timestamp.strftime(TIME_FORMAT),
                'contents': self.contents,
                'priority': self.priority}

    @classmethod
    def create(cls, timestamp: str, contents: str, priority: str):
        if not TIME_RE.fullmatch(timestamp):
            return False
        timestamp = datetime.strptime(timestamp, TIME_FORMAT)

        todo = cls(timestamp=timestamp,
                   contents=contents,
                   priority=priority)
        try:
            with session_scope() as session:
                session.add(todo)
            return True
        except IntegrityError as ie:
            logger.error(f'{ie} data create error')
            return False

    @classmethod
    def update(cls, timestamp: str, contents: str, priority: str):
        if not TIME_RE.fullmatch(timestamp):
            return False
        timestamp = datetime.strptime(timestamp, TIME_FORMAT)

        try:
            with session_scope() as session:
                todo = session.query(cls).filter(
                    cls.timestamp == timestamp).first()
                if todo is None:
                    raise DataUpdateError
                todo.contents = contents
                todo.priority = priority
            return True
        except DataUpdateError as de:
            logger.error(f'{de} {de.message}')
            return False

    @classmethod
    def get(cls, timestamp: str):
        if not TIME_RE.fullmatch(timestamp):
            return False
        timestamp = datetime.strptime(timestamp, TIME_FORMAT)

        with session_scope() as session:
            todo = session.query(cls).filter(
                cls.timestamp == timestamp).first()
        if todo is None:
            return None
        return todo

    @classmethod
    def get_all(cls):
        with session_scope() as session:
            todo = session.query(cls).all()
        if todo is None:
            return None
        todo.reverse()
        return todo

    @classmethod
    def delete(cls, timestamp: str):
        if not TIME_RE.fullmatch(timestamp):
            return False
        timestamp = datetime.strptime(timestamp, TIME_FORMAT)

        with session_scope() as session:
            todo = session.query(cls).filter(
                cls.timestamp == timestamp).first()
            if todo is None:
                return False
            session.delete(todo)
        return True

    def save(self):
        with session_scope() as session:
            session.add(self)
