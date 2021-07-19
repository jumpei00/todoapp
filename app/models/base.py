from contextlib import contextmanager
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

logger = logging.getLogger(__name__)
Base = declarative_base()


def db_engine(driver: str, db_name: str):
    return create_engine(f'{driver}:///{db_name}')


def init_db(driver: str, db_name: str):
    engine = db_engine(driver, db_name)
    Base.metadata.create_all(bind=engine)

    global Session
    Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f'{e} session error')
        raise
    finally:
        session.expire_on_commit = True
