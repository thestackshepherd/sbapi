import os

from sqlalchemy import create_engine, URL
import dotenv

dotenv.load_dotenv()

DATABASE_USERNAME   = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD   = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST       = os.getenv("DATABASE_HOST")
DATABASE_PORT       = os.getenv("DATABASE_PORT")
DATABASE_NAME       = os.getenv("DATABASE_NAME")

postgresurl = URL.create(
    drivername="postgresql+psycopg",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME,
)

engine = create_engine(postgresurl)
