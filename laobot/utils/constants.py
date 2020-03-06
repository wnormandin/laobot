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
ACTION_WAIT_TIME = int(os.environ.get('LAOBOT_ACTION_INTERVAL', 30))

SERVER_HOST = os.environ.get('LAOBOT_SERVER_HOST', 'localhost')
SERVER_PORT = int(os.environ.get('LAOBOT_SERVER_PORT', 9999))
PIDFILE = os.path.abspath(os.path.join(tempfile.gettempdir(), 'laobot.pid'))
THREADS_PER_RUNNER = 2
CORPUS_DIRECTORY = os.environ.get('LAOBOT_CORPUS_DIR', r'Z:\Git\untitled1\data\lao')

CELERY_REDIS_DB = os.environ.get('LAOBOT_REDIS_DB', '1')
redis_host = os.environ.get('LAOBOT_REDIS_HOST', 'localhost')
redis_port = os.environ.get('LAOBOT_REDIS_PORT', '6379')
redis_password = os.environ.get('LAOBOT_REDIS_PASSWORD', '')
CELERY_REDIS_URL = f'redis://:{redis_password}@{redis_host}:{redis_port}/{CELERY_REDIS_DB}'
CELERY_BROKER_URL = CELERY_REDIS_URL
CELERY_RESULT_BACKEND = CELERY_REDIS_URL

# Specify a MySQL DB host, or a sqlite DB host for testing
db_schema = 'laobot'
charset = 'utf8mb4'
DB_HOST = os.environ.get('LAOBOT_DB_HOST')
DB_PORT = os.environ.get('LAOBOT_DB_PORT', 3306)
DB_USER = os.environ.get('LAOBOT_DB_USER')
DB_PASS = os.environ.get('LAOBOT_DB_PASSWORD')
if not all((DB_HOST, DB_USER, DB_PASS)):
    DB_URL = os.environ.get('LAOBOT_DB_URL', 'sqlite:///test.sqlite')
else:
    DB_URL = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{db_schema}?charset={charset}'

engine = db.create_engine(DB_URL)
Session = sessionmaker(bind=engine)
