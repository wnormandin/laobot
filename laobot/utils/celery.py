from celery import Celery
from . import constants, RedditJobRunner, test_task
from ..db import SubredditActions, SubredditFilters


app = Celery('laobot', broker=constants.CELERY_BROKER_URL)


@app.task
def run_test():
    test_task()


@app.task
def run_job(subreddit_name, action=SubredditActions.scrape, subreddit_filter=SubredditFilters.hot):
    runner = RedditJobRunner(subreddit_name=subreddit_name, action=action, subreddit_filter=subreddit_filter)
    runner.dispatch()


def get_app_info():
    response = {}
    inspection = app.control.inspect()
    response['stats'] = inspection.stats()
    response['tasks'] = inspection.registered()
    response['active'] = inspection.active()
    response['scheduled'] = inspection.scheduled()
    return response


def ping():
    inspection = app.control.inspect()
    return inspection.ping()
