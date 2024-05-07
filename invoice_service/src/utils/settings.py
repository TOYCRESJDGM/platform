import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get('ENVIRONMENT')
APP_PORT= os.environ.get('APP_PORT')

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_USER_NAME = os.environ.get('DB_USER_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

