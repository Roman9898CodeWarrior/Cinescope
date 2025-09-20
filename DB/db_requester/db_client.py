from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

from resources.creds import DBCreds

DB_HOST = DBCreds.DB_HOST
DB_PORT = DBCreds.DB_PORT
DB_NAME = DBCreds.DB_NAME
DB_USERNAME = DBCreds.DB_USERNAME
DB_PASSWORD = DBCreds.DB_PASSWORD

engine = create_engine(f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()