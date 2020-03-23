# LAOBot
[Homepage][3] | [Github][2] | last updated v0.0.1

## Configuration
This package uses [praw][1], a **praw.ini** file must be created containing Reddit OAuth credentials

The following values may be set in the environment to configure LAOBot 

##### Bot Behavior
* LAOBOT_TEST (default = **0**)
* LAOBOT_CORPUS_DIR - directory containing the television script text files from which markov chains and substring searches will operate
* LAOBOT_ACTION_INTERVAL (default = **30**s)
* LAOBOT_SUBMISSION_SAMPLE_SIZE
* LAOBOT_COMMENT_SAMPLE_SIZE (default = **50** comments)
* LAOBOT_COMMENT_MIN_UPVOTES (default = **5** upvotes)
* LAOBOT_DEFAULT_SUBREDDITS (default = **television,movies**)
* LAOBOT_MAX_COMMENTS_PER_RUNNER
* LAOBOT_COMMENT_TEMPLATE_DIR
* LAOBOT_COMMENT_TEMPLATE_FILE

##### Celery Broker Configuration
* LAOBOT_REDIS_DB (default = **1**)
* LAOBOT_REDIS_HOST (default = **localhost**)
* LAOBOT_REDIS_PORT (default = **6379**)
* LAOBOT_REDIS_PASSWORD (default = **""**)

##### Database Configuraton
* LAOBOT_DB_URL (replaces the other DB options, default = **sqlite:///test.sqlite** when other options missing)
* LAOBOT_DB_HOST
* LAOBOT_DB_PORT
* LAOBOT_DB_USER
* LAOBOT_DB_PASSWORD

##### LAOBot Server
* LAOBOT_SERVER_HOST
* LAOBOT_SERVER_PORT

##### User-Agent 
Reddit strongly encourages informative user-agent strings.  The following options will drive the user-agent string used by LAOBot
* LAOBOT_AUTHOR (provide this as a reddit user, e.g. **"u/pokeybill"**)
* LAOBOT_HOMEPAGE

## Running the bot
* Start Redis
* Start celery workers
  * celery -A laobot.utils.celery worker --loglevel=debug -P solo
* Start LAOBot server (blocking command)
  * laobot start
  
[1]: https://praw.readthedocs.io/en/latest/
[2]: https://github.com/wnormandin/laobot
[3]: https://pokeybots.com/laobot.html