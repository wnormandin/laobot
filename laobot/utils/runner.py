import logging

from ..utils import subreddit_top_n
from ..db import (
    Functions,
    SubredditActions,
    JobStatus,
)

from ..quote_generator import find_substring
logger = logging.getLogger(__name__)


class RedditJobRunner:
    def __init__(self, subreddit_name, action, subreddit_filter='hot', scrape_count=None):
        self.subreddit = Functions.get_or_create_subreddit(subreddit_name)
        self.job = Functions.create_job(self.subreddit.name, action, subreddit_filter=subreddit_filter,
                                        scrape_count=scrape_count)
        self.event(f'Job {self.job.uuid} started')
        self.job_started()

    def dispatch(self):
        if self.job.action == SubredditActions.scrape:
            self.do_scrape()
        elif self.job.action == SubredditActions.comment:
            self.do_comment()

    def get_submissions(self):
        submissions = subreddit_top_n(
            self.job.subreddit,
            self.job.filter,
            self.job.scrape_count
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
        for comment in submission['comments']:
            if len(comment.body) < 50:
                continue

            path, text = find_substring(comment['body'][:50])
            if path:
                self.event(f'Found comment {comment["name"]} in {path}: {text}')

    def do_comment(self):
        pass

    def event(self, message):
        return Functions.create_event(message=message, job=self.job)

    def job_complete(self):
        Functions.set_job_status(self.job, JobStatus.complete)

    def job_started(self):
        Functions.set_job_status(self.job, JobStatus.in_progress)

    def job_error(self):
        Functions.set_job_status(self.job, JobStatus.error)

    def check_item(self, item):
        if not Functions.already_processed(item.fullname):
            Functions.mark_item_processed(item_name=item.fullname, job=self.job)
