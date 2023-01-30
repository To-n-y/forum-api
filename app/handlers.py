import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, Form, Request

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import HTMLResponse

from app.auth import check_auth_token
from app.forms import UserLoginForm, UserCreateForm
from app.models import connect_db, User, AuthToken, Topic, Message
from app.utils import get_hash_password

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

signed_user_id = None


@router.get("/")
async def home(
    database=Depends(connect_db), response_class=HTMLResponse, request: Request = None
):
    global signed_user_id
    topic_list = database.query(Topic).all()
    topic_user_dict = {}
    for topic in topic_list:
        user = database.query(User).filter(User.id == topic.user_id).one()
        topic_user_dict[topic] = user
    ln = len(topic_list)
    signed_user = database.query(User).filter(User.id == signed_user_id).one_or_none()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "topic_dict": topic_user_dict,
            "l": ln,
            "signed_user": signed_user,
        },
    )


@router.get("/registration", name="registration")
def registration_1():
    return templates.TemplateResponse("registration.html", {"request": {"user": None}})


@router.get("/sign_in", name="sign_in")  # 1 - войти, 0 - выйти
def registration_2(to: int, request: Request = None, database=Depends(connect_db)):
    if to == 1:
        return templates.TemplateResponse("sign_in.html", {"request": {"user": None}})
    else:
        global signed_user_id
        signed_user_id = None
        topic_list = database.query(Topic).all()
        topic_user_dict = {}
        for topic in topic_list:
            user = database.query(User).filter(User.id == topic.user_id).one()
            topic_user_dict[topic] = user
        ln = len(topic_list)
        signed_user = (
            database.query(User).filter(User.id == signed_user_id).one_or_none()
        )
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "topic_dict": topic_user_dict,
                "l": ln,
                "signed_user": signed_user,
            },
        )


@router.get("/profile", name="profile")
def profile(user_id: int, database=Depends(connect_db)):
    global signed_user_id  # curr_user_id - id of user who is signed in
    curr_user = (
        database.query(User).filter(User.id == user_id).one_or_none()
    )  # user_id - id of user whose profile is opened
    signed_user = database.query(User).filter(User.id == signed_user_id).one_or_none()
    if signed_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authorization required"
        )
    if curr_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
    else:
        return templates.TemplateResponse(
            "profile.html",
            {"request": {"user": None}, "user": curr_user, "signed_user": signed_user},
        )


@router.get("/user", name="user:get")
def get_user(
    token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)
):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
    }


@router.get("/topic", name="topic")
def topic(topic_id: int, database=Depends(connect_db)):
    global signed_user_id
    curr_topic = database.query(Topic).filter(Topic.id == topic_id).one_or_none()
    if signed_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="You are not authorized!"
        )
    elif curr_topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
        )
    message_list = database.query(Message).filter(Message.topic_id == topic_id).all()
    return templates.TemplateResponse(
        "topic.html",
        {
            "request": {"user": None},
            "curr_topic": curr_topic,
            "message_list": message_list,
        },
    )


@router.post("/post_topic", name="post_create")
def post_create(
    topic_name=Form(),
    user_id=Form(),
    database=Depends(connect_db),
    request: Request = None,
):
    user = database.query(User).filter(User.id == user_id).one()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        new_topic = Topic(name=topic_name, user_id=user_id)
        database.add(new_topic)
        database.commit()
        global signed_user_id
        topic_list = database.query(Topic).all()
        topic_user_dict = {}
        for topic in topic_list:
            user = database.query(User).filter(User.id == topic.user_id).one()
            topic_user_dict[topic] = user
        ln = len(topic_list)
        signed_user = (
            database.query(User).filter(User.id == signed_user_id).one_or_none()
        )
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "topic_dict": topic_user_dict,
                "l": ln,
                "signed_user": signed_user,
            },
        )


@router.post("/sign_in", name="sign_in")
def user_create_sign(
    user_password=Form(),
    user_name=Form(),
    database=Depends(connect_db),
    request: Request = None,
):
    curr_user = database.query(User).filter(User.name == user_name).one_or_none()
    if curr_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif curr_user.password != user_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="password is incorrect"
        )
    else:
        global signed_user_id
        signed_user_id = curr_user.id
        topic_list = database.query(Topic).all()
        topic_user_dict = {}
        for topic in topic_list:
            user = database.query(User).filter(User.id == topic.user_id).one()
            topic_user_dict[topic] = user
        ln = len(topic_list)
        signed_user = (
            database.query(User).filter(User.id == signed_user_id).one_or_none()
        )
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "topic_dict": topic_user_dict,
                "l": ln,
                "signed_user": signed_user,
            },
        )


@router.post("/post_user", name="user_create")
def user_create_post(
    user_email=Form(),
    user_password1=Form(),
    user_password2=Form(),
    user_name=Form(),
    user_surname=Form(),
    database=Depends(connect_db),
    request: Request = None,
):
    if user_password2 == user_password1:
        u = database.query(User).filter(User.name == user_name).one_or_none()
        if u is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User already exists"
            )
        new_user = User(
            name=user_name,
            email=user_email,
            password=user_password1,
            surname=user_surname,
        )
        database.add(new_user)
        database.commit()
        global signed_user_id
        signed_user_id = new_user.id
        topic_list = database.query(Topic).all()
        topic_user_dict = {}
        for topic in topic_list:
            user = database.query(User).filter(User.id == topic.user_id).one()
            topic_user_dict[topic] = user
        ln = len(topic_list)
        signed_user = (
            database.query(User).filter(User.id == signed_user_id).one_or_none()
        )
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "topic_dict": topic_user_dict,
                "l": ln,
                "signed_user": signed_user,
            },
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Password not confirmed"
        )


@router.post("/post_message", name="message_create")
def message_create(topic_id=Form(), message_text=Form(), database=Depends(connect_db)):
    new_message = Message(topic_id=topic_id, text=message_text)
    database.add(new_message)
    database.commit()
    curr_topic = database.query(Topic).filter(Topic.id == topic_id).one_or_none()
    curr_topic.message_count += 1
    database.commit()
    print(curr_topic.message_count)
    return topic(topic_id=topic_id, database=database)


@router.post("/login", name="user:login")
def login(
    user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)
):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_form.email} not found",
        )
    if user.password != get_hash_password(user_form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )
    token = uuid.uuid4().hex
    new_token = AuthToken(token=token, user_id=user.id)
    database.add(new_token)
    database.commit()
    return {"access_token": new_token.token}


@router.post("/user", name="user:create")
def create_user(
    user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)
):
    exists_user = database.query(User).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    new_user = User(
        email=user.email,
        password=get_hash_password(user.password),
        name=user.name,
        surname=user.surname,
    )
    database.add(new_user)
    database.commit()
    return {"created_user_id": new_user.id}
