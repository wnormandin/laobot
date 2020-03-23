__version__ = '0.0.2'
import logging
import pymysql
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()
logging.basicConfig(level=logging.INFO)
load_dotenv()
