from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movies(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
    location = Column()
    published = Column(Boolean)
    rating = Column(Integer)
    genre_id = Column(Integer)
    created_at = Column(TIMESTAMP)