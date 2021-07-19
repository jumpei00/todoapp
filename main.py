import logging

from conf import config
from app.models import base
from app.controllers import web
from log import log

# variable for deploy
app = web.app

# log and database setting
log.logging_setting()
base.init_db(driver=config.db_driver, db_name=config.db_name)


if __name__ == '__main__':
    """for debag
    flask web server will run if 'python main.py'
    """
    logger = logging.getLogger(__name__)
    logger.info('web server start')
    web.run()
