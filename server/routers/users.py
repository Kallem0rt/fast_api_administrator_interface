import logging
import os
import sys
from pathlib import Path

from fastapi import APIRouter, Form
from fastapi import Depends, HTTPException
from fastapi.responses import Response, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.tasks import repeat_every
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import sessionmaker

from server.core.connection import db_connect
from server.core.models.users import users as user_list
from server.shemas import users
from server.utils import users as users_utils
from server.utils.depenecies import get_current_user
from server.utils.users import delete_user, remove_expires_token

path = Path(".")

router = APIRouter()

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=Log_Format, level=logging.INFO)
logger = logging.getLogger()


@router.post("/sign-up")
async def create_user(name: str = Form(), password: str = Form(), email: str = Form()):
    db_user = await users_utils.get_user_by_email(email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(
        user={"name": name, "password": password, "email": email}
    )


# response_model=users.TokenBase
@router.post("/auth", response_model=users.TokenBase)
async def auth(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user.hashed_password
    ):
        logger.info(f"Incorrect password: {form_data.password}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    tokens = await users_utils.create_user_token(user_id=user.id)
    logger.info(f"Auth user: {user.name}")
    response.set_cookie(key="Auth", value=tokens.token)
    return {"name": user.name, "expires": tokens.expires}


@router.post("/secure-form", response_model=users.UserBase)
def read_users_me(current_user: users.User = Depends(get_current_user)):
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(path, f"templates/users"), encoding="utf-8"
        ),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("secure_form.html")
    rendered_page = template.render(user=current_user)
    return HTMLResponse(rendered_page)


@router.get("/create-users")
def rec_webhook(current_user: users.User = Depends(get_current_user)):
    logger.info(current_user)
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(path, f"templates/users"), encoding="utf-8"
        ),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("create.html")
    rendered_page = template.render()
    return HTMLResponse(rendered_page)


@router.get("/auth-form")
def rec_webhook():
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(path, f"templates/users"), encoding="utf-8"
        ),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("auth.html")
    rendered_page = template.render()
    return HTMLResponse(rendered_page)


@router.get("/secure")
def rec_webhook():
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(path, f"templates/users"), encoding="utf-8"
        ),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("secure.html")
    rendered_page = template.render()
    return HTMLResponse(rendered_page)


@router.post("/delete-user")
def rec_webhook(
    user_id: int = Form(), current_user: users.User = Depends(get_current_user)
):
    logger.info(
        f"Удаляеться пользователь {user_id} пользователем {current_user['name']}"
    )

    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(user_list).filter(user_list.id == user_id).all()
    if len(list(users)) == 1:
        raise HTTPException(
            status_code=400, detail="Запрещено удалять единственного пользователя"
        )
    user = delete_user(user_id)
    return f"Пользователь {user_id} удален пользователем {current_user['name']}"


@router.post("/get-all-users")
def rec_webhook(current_user: users.User = Depends(get_current_user)):
    engine = db_connect()
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    logger.info(f"Просмотр пользователей пользователем {current_user['name']}")
    users_list = list()
    if current_user["superuser"]:
        users_list = session.query(user_list).all()
    session.close()
    return users_list


@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 24 hour
def remove_expired_tokens_task() -> None:
    remove_expires_token()


@router.on_event("startup")
async def check_users() -> None:
    await check_users_exists()


async def check_users_exists():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(user_list).all()
    session.close()
    if not users:
        return await users_utils.create_user(
            user={
                "name": "Test",
                "password": "Test",
                "email": "Test@mail.com",
                "superuser": 1,
            }
        )
