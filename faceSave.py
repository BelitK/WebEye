from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, insert
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FaceData(Base):
    __tablename__ = 'facedb'
    id = Column(Integer, primary_key=True)
    face_encode = Column(JSON)

from sqlalchemy import create_engine

engine = create_engine("postgresql://belit:12897@localhost:5432/FaceDb")

from sqlalchemy.orm import sessionmaker
def insert_encode(liste):
    jsondata=  liste
    sqlaclhey.insert(face_encode(jsondata))

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)