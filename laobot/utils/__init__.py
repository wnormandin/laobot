import praw
import json
import logging

from .constants import USER_AGENT, BOT_NAME


logger = logging.getLogger(__name__)


def json_log(json_obj, log_level='INFO', **json_kwargs):
    method = getattr(logger, log_level.lower())
    method(json.dumps(json_obj, **json_kwargs))


def get_reddit():
    return praw.Reddit(BOT_NAME, user_agent=USER_AGENT)


def subreddit_top_n(subreddit_name, subreddit_filter='hot', n=5):
    reddit = get_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    items = getattr(subreddit, subreddit_filter)(limit=n)
    return [{s.title: (f'u/{s.author}', s.score)} for s in items]


def test_task():
    from ..db import create_event
    top_5 = subreddit_top_n('television')
    return create_event(f'Fetched {len(top_5)} submissions')
