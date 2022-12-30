from fastapi import APIRouter, Body, Depends, HTTPException, Form
from starlette import status
from starlette.responses import HTMLResponse, FileResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth import check_auth_token
from forms import UserLoginForm, UserCreateForm
from models import connect_db, User, AuthToken, Topic, Message
from utils import get_hash_password
import uuid

router = APIRouter()

# router.mount('/static', FileResponse('static'), name='static')
templates = Jinja2Templates(directory='templates')


@router.get('/')
def home(database=Depends(connect_db)):
    topic_list = database.query(Topic).all()
    return templates.TemplateResponse('home.html', {'request': {'user': None}, 'topic_list': topic_list})


@router.get('/topic', name='topic')
def topic(topic_id: int, database=Depends(connect_db)):
    curr_topic = database.query(Topic).filter(Topic.id == topic_id).one_or_none()
    if curr_topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Topic not found'
        )
    message_list = database.query(Message).filter(Message.topic_id == topic_id).all()
    return templates.TemplateResponse('topic.html',
                                      {'request': {'user': None}, 'curr_topic': curr_topic,
                                       'message_list': message_list})


@router.post('/post_message_data', name='message_create')
def message_create(topic_id=Form(), message_text=Form(), database=Depends(connect_db)):
    message = Message(topic_id=topic_id, text=message_text)
    database.add(message)
    database.commit()
    message_list = database.query(Message).filter(Message.topic_id == topic_id).all()
    curr_topic = database.query(Topic).filter(Topic.id == topic_id).one_or_none()
    return templates.TemplateResponse('topic.html',
                                      {'request': {'user': None}, 'curr_topic': curr_topic,
                                       'message_list': message_list})


@router.post('/login', name='user:login')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with email {user_form.email} not found'
        )
    if user.password != get_hash_password(user_form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password'
        )
    token = uuid.uuid4().hex
    new_token = AuthToken(token=token, user_id=user.id)
    database.add(new_token)
    database.commit()
    return {'access_token': new_token.token}


@router.post('/user', name='user:create')
def create_user(user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)):
    exists_user = database.query(User).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    new_user = User(email=user.email,
                    password=get_hash_password(user.password),
                    name=user.name,
                    surname=user.surname
                    )
    database.add(new_user)
    database.commit()
    return {"created_user_id": new_user.id}


@router.get('/user', name='user:get')
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    return {"id": user.id, "email": user.email, "name": user.name, "surname": user.surname}
