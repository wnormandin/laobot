import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session
from sqlalchemy.ext.declarative import declarative_base
from .utils.constants import Session, engine, COMMENT_SAMPLE_SIZE


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


class TimestampedRecord(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Event(TimestampedRecord):
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


class Job(TimestampedRecord):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100), unique=True, default=get_uuid)
    subreddit = Column(String(100), ForeignKey('subreddits.name'))

    action = Column(Enum(SubredditActions))
    filter = Column(Enum(SubredditFilters))
    status = Column(Enum(JobStatus), default=JobStatus.new)

    scrape_count = Column(Integer, nullable=True, default=COMMENT_SAMPLE_SIZE)


class ProcessedItem(Base):
    __tablename__ = 'processed_items'

    name = Column(String(100), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))

    job = relationship(Job)


class Comment(TimestampedRecord):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100), unique=True, default=get_uuid)
    parent_id = Column(String(100), ForeignKey('processed_items.name'))
    permalink = Column(String(196))


class Functions:
    @staticmethod
    def already_processed(item_name) -> bool:
        session = get_session()
        item = session.query(ProcessedItem).filter_by(name=item_name).first()
        return bool(item)

    @staticmethod
    def mark_item_processed(item_name, job_id) -> bool:
        session = get_session()
        item = ProcessedItem(name=item_name, job_id=job_id)
        session.add(item)
        session.commit()
        return True

    @staticmethod
    def track_comment(comment, parent_id):
        session = get_session()
        item = Comment(parent_id=parent_id, permalink=f'https://reddit.com{comment.permalink}')
        session.add(item)
        session.commit()
        return item.permalink

    @staticmethod
    def create_event(message, job_id=None) -> int:
        session = get_session()
        event = Event(message=message, job_id=job_id)
        session.add(event)
        session.commit()

        return event.id

    @staticmethod
    def create_job(subreddit, action, subreddit_filter=SubredditFilters.hot, scrape_count=None) -> Job:
        session = get_session()
        job = Job(subreddit=subreddit, filter=subreddit_filter, action=action,
                  scrape_count=scrape_count)
        session.add(job)
        session.commit()
        return job.id

    @staticmethod
    def set_job_status(job_id, status=JobStatus.new) -> None:
        session = get_session()
        job = session.query(Job).get(job_id)
        job.status = status
        session.add(job)
        session.commit()

    @staticmethod
    def get_or_create_subreddit(subreddit_name) -> Subreddit:
        session = get_session()
        subreddit = session.query(Subreddit).filter_by(name=subreddit_name).first()
        if subreddit is None:
            subreddit = Subreddit(name=subreddit_name)
            session.add(subreddit)
            session.commit()
        return subreddit
