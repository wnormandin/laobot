import praw
import json
import logging
from concurrent.futures import ThreadPoolExecutor

from .constants import USER_AGENT, BOT_NAME
from ..db import (
    create_event,
    create_job,
    set_job_status,
    get_or_create_subreddit,
    Event,
    SubredditActions,
    SubredditFilters,
    JobStatus,
    Job,
    Subreddit
)
from ..quote_generator import generate_complete_model, find_substring
#model = generate_complete_model()


logger = logging.getLogger(__name__)


def json_log(json_obj, log_level='INFO', **json_kwargs):
    method = getattr(logger, log_level.lower())
    method(json.dumps(json_obj, **json_kwargs))


def get_reddit():
    return praw.Reddit(BOT_NAME, user_agent=USER_AGENT)


class RedditJobRunner:
    def __init__(self, subreddit_name, action, subreddit_filter='hot'):
        self.subreddit = get_or_create_subreddit(subreddit_name)
        self.job = create_job(self.subreddit.name, action, subreddit_filter=subreddit_filter)
        self.event(f'Job {self.job.uuid} started')
        self.job_started()

    def dispatch(self):
        if self.job.action == SubredditActions.scrape:
            self.do_scrape()
        elif self.job.action == SubredditActions.comment:
            self.do_comment()

    def get_submissions(self):
        submissions = subreddit_top_n(
            self.job.subreddit.name,
            self.job.filter,
            self.job.scrape_count or 1
        )
        self.event(f'Fetched submissions from subreddit {self.subreddit.name}')
        return submissions

    def do_scrape(self):
        try:
            for submission in self.get_submissions():
                self.process_submission(submission)
        except Exception as e:
            self.event(f'Error: {str(e)}')
            logger.exception(str(e))
            self.job_error()
        else:
            self.event(f'Job {self.job.uuid} Completed')
            self.job_complete()

    def process_submission(self, submission):
        for comment in submission.comments:
            if len(comment.body) < 50:
                continue

            path, text = find_substring(comment.body[:50])
            if path:
                self.event(f'Found comment {comment.name} in {path}: {text}')

    def do_comment(self):
        pass

    def event(self, message):
        return create_event(message=message, job=self.job)

    def job_complete(self):
        set_job_status(self.job, JobStatus.complete)

    def job_started(self):
        set_job_status(self.job, JobStatus.started)

    def job_error(self):
        set_job_status(self.job, JobStatus.error)


def subreddit_top_n(subreddit_name, subreddit_filter='hot', n=5):
    reddit = get_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    items = getattr(subreddit, subreddit_filter)(limit=n)
    return [{s.title: (f'u/{s.author}', s.score)} for s in items]


def test_task():
    top_5 = subreddit_top_n('television')
    return create_event(f'Fetched {len(top_5)} submissions')
