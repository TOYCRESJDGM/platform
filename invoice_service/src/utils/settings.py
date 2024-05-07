import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get('ENVIRONMENT')
APP_PORT= os.environ.get('APP_PORT')

URL_SCRAPPER= os.environ.get('URL_SCRAPPER')

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

