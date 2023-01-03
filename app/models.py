from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from app.config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
    session = Session(bind=engine.connect())
    return session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    datetime = Column(String, default=datetime.utcnow())


class AuthToken(Base):
    __tablename__ = 'auth_tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String)
    datetime = Column(String, default=datetime.utcnow())


class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    message_count = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    datetime = Column(String, default=datetime.utcnow())


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    likes = Column(Integer, default=0)
    text = Column(String)
    answered_message_id = Column(Integer, ForeignKey('messages.id'), default=None)
    datetime = Column(String, default=datetime.utcnow())
