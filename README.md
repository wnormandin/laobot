# LAOBot
last updated v0.0.1

## Configuration
The following values may be set in the environment to configure LAOBot 

* LAOBOT_TEST (default=0/False)
* LAOBOT_REDIS_DB (default=1)
* LAOBOT_REDIS_HOST (default=localhost)
* LAOBOT_REDIS_PORT (default=6379)
* LAOBOT_CORPUS_DIR - directory containing the television script text files from which the bot generates and detects content
* LAOBOT_DB_URL (default=sqlite:///test.sqlite)
* LAOBOT_ACTION_INTERVAL
* LAOBOT_SERVER_HOST - host used by the LAOBot server (default=localhost)
* LAOBOT_SERVER_PORT - sets the local port over which the LAOBot server will listen

Reddit strongly encourages informative user-agent strings.  The following options will drive the user-agent string used by LAOBot
* LAOBOT_AUTHOR (provide this as a reddit user, e.g. **"u/pokeybill"**)
* LAOBOT_HOMEPAGE

## Running the bot
* Start Redis
* Start celery workers
  * celery -A laobot.utils.celery worker --loglevel=debug -P solo
* Start LAOBot server (blocking command)
  * laobot start