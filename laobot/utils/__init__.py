import enum
import praw
import json
import logging

from .constants import USER_AGENT, BOT_NAME
from ..db import SubredditFilters


logger = logging.getLogger(__name__)


class RedditTypePrefix(enum.Enum):
    comment = 't1'
    acount = 't2'
    link = 't3'
    message = 't4'
    subreddit = 't5'
    award = 't6'


def get_thing_type(thing):
    for member in RedditTypePrefix:
        if thing.startswith(member.value):
            return member


def json_log(json_obj, log_level='INFO', **json_kwargs):
    method = getattr(logger, log_level.lower())
    method(json.dumps(json_obj, **json_kwargs))


def get_reddit():
    return praw.Reddit(BOT_NAME, user_agent=USER_AGENT)


def subreddit_top_n(subreddit_name, subreddit_filter=SubredditFilters.hot, n=5):
    reddit = get_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    items = getattr(subreddit, subreddit_filter.value)(limit=n)
    return [{s.title: (f'u/{s.author}', s.score)} for s in items]


def test_task():
    from ..db import Functions
    top_5 = subreddit_top_n('television')
    return Functions.create_event(f'Fetched {len(top_5)} submissions')
