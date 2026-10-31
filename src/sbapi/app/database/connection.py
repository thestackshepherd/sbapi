import os

import dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

DATABASE_USERNAME   = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD   = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST       = os.getenv("DATABASE_HOST")
DATABASE_PORT       = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME       = os.getenv("DATABASE_NAME")

postgresurl = URL.create(
    drivername="postgresql+psycopg",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT) if DATABASE_PORT else None,
    database=DATABASE_NAME,
)

engine = create_engine(postgresurl)

SessionLocal = sessionmaker(bind=engine)
