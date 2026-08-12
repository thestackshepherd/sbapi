import os

from sqlalchemy import create_engine
import dotenv

dotenv.load_dotenv()

DATABASE_USERNAME = os.getenv('DATABASE_URL')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

