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

# LAOBot Server configuration
SERVER_HOST = os.environ.get('LAOBOT_SERVER_HOST', 'localhost')
SERVER_PORT = int(os.environ.get('LAOBOT_SERVER_PORT', 9999))
PIDFILE = os.path.abspath(os.path.join(tempfile.gettempdir(), 'laobot.pid'))

# Bot activity tuning
ACTION_WAIT_TIME = int(os.environ.get('LAOBOT_ACTION_INTERVAL', 30))

# Dictates the number of comments per submission to parse (with children)
COMMENT_SAMPLE_SIZE = int(os.environ.get('LAOBOT_COMMENT_SAMPLE_SIZE', 50))

# Minimum score for a comment to be considered
COMMENT_MIN_UPVOTES = int(os.environ.get('LAOBOT_COMMENT_MIN_UPVOTES', 5))

# Number of threads to use per RedditJobRunner instance
THREADS_PER_RUNNER = int(os.environ.get('LAOBOT_THREADS_PER_RUNNER', 2))

# Directory containing text files which will form the corpus
# for markov generation and substring searches
CORPUS_DIRECTORY = os.environ.get('LAOBOT_CORPUS_DIR', r'Z:\Git\untitled1\data\lao')

# Provide comma-separated subreddits to be crawled as part of the default job
DEFAULT_SUBREDDITS = os.environ.get('LAOBOT_DEFAULT_SUBREDDITS', 'television,movies').split(',')

# Celery configuration
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
DB_URL = os.environ.get('LAOBOT_DB_URL')

if DB_URL or not all((DB_HOST, DB_USER, DB_PASS)):
    url = DB_URL or 'sqlite:///test.sqlite'
else:
    url = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{db_schema}?charset={charset}'

engine = db.create_engine(url)
Session = sessionmaker(bind=engine)
