from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
    session = Session(bind=engine.connect())
    session.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email VARCHAR, password VARCHAR, name VARCHAR, '
        'surname VARCHAR, '
        'datetime VARCHAR);')
    session.execute(
        'CREATE TABLE IF NOT EXISTS auth_tokens (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users, '
        'token VARCHAR, '
        'datetime VARCHAR);')
    session.commit()


if __name__ == '__main__':
    main()
