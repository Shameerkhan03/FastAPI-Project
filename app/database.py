import time
import psycopg2  # this library doesn't return column name when querying the database

# so we're importing this class to show us columns also
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy.engine.url import make_url

SQLALCHEMY_DATABASE_URL = settings.database_url
SQLALCHEMY_DATABASE_URL = make_url(SQLALCHEMY_DATABASE_URL).render_as_string(
    hide_password=False
)


# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # building connection to the database, using 'try' incase the connection fails (good practice)
# # if the database fails to connect (eg we gave wrong password). It will print out the error but
# # move on to executing the rest of our code on the server (all the crud operations etc)
# # to avoid this we use while loop. Until the database isn't connected we don't need to execute anything
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database="fastapi", user="postgres",
#                                 password="password", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print(f"Error: {error}")
#         # if fails to connect, it will stop for 2 seconds before checking the connection again
#         time.sleep(2)
#         # it will keep on checking the connection because we're in a while loop
