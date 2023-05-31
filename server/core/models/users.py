from sqlalchemy import Column, DateTime, Integer, VARCHAR, ForeignKey, create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///server.db', echo = True)
meta = MetaData()

class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(length=40))
    name = Column(VARCHAR(length=100))
    hashed_password = Column(VARCHAR(length=255))
    superuser = Column(Integer)
    is_active = Column(Integer)

class tokens_table(Base):
    __tablename__ = 'tokens_table'
    id = Column(Integer, primary_key=True)
    token = Column(VARCHAR(length=255))
    expires = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

create_users = Table('users',
    meta,
    Column("id", Integer, primary_key=True),
    Column("email", VARCHAR(length=40)),
    Column("name", VARCHAR(length=100)),
    Column("hashed_password", VARCHAR(length=255)),
    Column("superuser", Integer),
    Column("is_active", Integer))

create_tokens_table = Table('tokens_table',
    meta,
    Column("id", Integer, primary_key=True),
    Column("token", VARCHAR(length=255)),
    Column("expires", DateTime),
    Column("user_id", Integer, ForeignKey("users.id")))

meta.create_all(engine)

