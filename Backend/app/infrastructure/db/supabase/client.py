import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

load_dotenv()


engine =create_engine(os.environ["DATABASE_URL"],poolclass=NullPool)
#conn = psycopg2.connect(os.environ["DATABASE_URL"])
#conn.autocommit = True 