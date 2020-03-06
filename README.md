# LAOBot

## Running the bot
1) Start Redis
2) Start celery workers
  * celery -A laobot.utils.celery worker --loglevel=debug -P solo
3) Start LAOBot server (blocking command)
  * laobot start