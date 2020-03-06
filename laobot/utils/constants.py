import os
import tempfile

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from laobot import __version__

BOT_AUTHOR = os.environ.get('LAOBOT_AUTHOR', 'u/pokeybill')
BOT_HOMEPAGE_URL = os.environ.get('LAOBOT_HOMEPAGE', 'https://pokeybots.com/laobot.html')
USER_AGENT = f"LAO Bot v{__version__} by {BOT_AUTHOR}: {BOT_HOMEPAGE_URL}"
BOT_NAME = 'laobot'
TEST = bool(int(os.environ.get('LAOBOT_TEST', 0)))

# Bot activity tuning
#ACTION_WAIT_TIME = 30 if TEST else (60 * 60 * 6)
ACTION_WAIT_TIME = 30
SERVER_HOST = 'localhost'
SERVER_PORT = 9999
PIDFILE = os.path.abspath(os.path.join(tempfile.gettempdir(), 'laobot.pid'))
THREADS_PER_RUNNER = 2
CORPUS_DIRECTORY = r'Z:\Git\untitled1\data\lao'

CELERY_REDIS_DB = os.environ.get('LAOBOT_REDIS_DB', '1')
CELERY_REDIS_URL = f'redis://localhost:6379/{CELERY_REDIS_DB}'
CELERY_BROKER_URL = CELERY_REDIS_URL
CELERY_RESULT_BACKEND = CELERY_REDIS_URL

DB_URL = 'sqlite:///test.sqlite'
engine = db.create_engine(DB_URL)
Session = sessionmaker(bind=engine)
