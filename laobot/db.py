import uuid
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session
from sqlalchemy.ext.declarative import declarative_base
from .utils.constants import Session, engine


Base = declarative_base(bind=engine)


def get_session(**kwargs):
    return Session(**kwargs)


def get_uuid():
    return str(uuid.uuid4())


class SubredditFilters(enum.Enum):
    hot = 'hot'
    rising = 'rising'
    new = 'new'
    gilded = 'gilded'


class SubredditActions(enum.Enum):
    scrape = 'scrape'
    comment = 'comment'


class JobStatus(enum.Enum):
    new = 'new'
    in_progress = 'in_progress'
    error = 'error'
    complete = 'complete'


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    message = Column(String(192))

    job = relationship('Job', backref='events')


class Config(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    value = Column(String(192))


class Subreddit(Base):
    __tablename__ = 'subreddits'
    name = Column(String(100), primary_key=True)


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100), unique=True, default=get_uuid)
    subreddit = Column(String(100), ForeignKey('subreddits.name'))

    action = Column(Enum(SubredditActions))
    filter = Column(Enum(SubredditFilters))
    status = Column(Enum(JobStatus), default=JobStatus.new)

    scrape_count = Column(Integer, nullable=True)


def create_event(message, job=None):
    if job is not None:
        session = object_session(job)
    else:
        session = None

    if session is None:
        session = get_session()
    event = Event(message=message, job=job)
    session.add(event)
    session.commit()
    return event.id


def create_job(subreddit, action, subreddit_filter=SubredditFilters.hot):
    session = get_session()
    job = Job(subreddit=subreddit, filter=subreddit_filter, action=action)
    session.add(job)
    session.commit()
    return job


def set_job_status(job, status=JobStatus.new):
    session = object_session(job)
    if session is None:
        session = get_session()
    job.status = status
    session.add(job)
    session.commit()


def get_or_create_subreddit(subreddit_name):
    session = get_session()
    subreddit = session.query(Subreddit).filter_by(name=subreddit_name).first()
    if subreddit is None:
        subreddit = Subreddit(name=subreddit_name)
        session.add(subreddit)
        session.commit()
    return subreddit
