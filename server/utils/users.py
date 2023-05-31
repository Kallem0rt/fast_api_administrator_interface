import hashlib
import logging
import random
import string
import sys
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

from server.core.connection import db_connect
from server.core.models.users import tokens_table, users
from server.shemas import users as user_shema

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout,
                    format=Log_Format,
                    level=logging.INFO)
logger = logging.getLogger()


engine = db_connect()
Session = sessionmaker(bind=engine, autoflush=False)
session = Session()


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str,
                  salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str,
                      hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str):
    """ Возвращает информацию о пользователе """
    event = session \
        .query(users) \
        .filter(users.email == email) \
        .first()
    session.close()
    if event:
        return event
    else:
        return None


async def get_user_by_token(token: str):
    """ Возвращает информацию о владельце указанного токена """
    event = session \
        .query(tokens_table) \
        .filter(tokens_table.token == token) \
        .first()
    if event:
        tokens = session \
            .query(users) \
            .filter(users.id == event.user_id) \
            .first()
        session.close()
        return tokens
    else:
        session.close()
        return None


async def create_user_token(user_id: int):
    """ Создает токен для пользователя с указанным user_id """
    event = tokens_table(
        token=f"{uuid.uuid4()}",
        expires=datetime.now() + timedelta(weeks=2),
        user_id=user_id
    )
    session.add(event)
    session.commit()
    session.flush()
    logger.info(event.token)
    return event


async def create_user(user: user_shema.UserCreate):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user['password'], salt)
    event = users(
        email=user['email'], 
        name=user['name'], 
        hashed_password=f"{salt}${hashed_password}",
        is_active=1,
        superuser=0 if not user['superuser'] else 1)
    session.add(event)
    session.commit()
    token = await  create_user_token(event.id)
    token_dict = {"token": token.token, "expires": token.expires}
    return token_dict

def delete_user(user_id: int):
    user = session \
        .query(users) \
        .filter(users.id == user_id) \
        .delete()
    session.commit()
    return user

def remove_expires_token():
    tokens = session \
        .query(tokens_table) \
        .filter(tokens_table.expires < datetime.now()) \
        .delete()
    session.commit()