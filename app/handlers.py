from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from auth import check_auth_token
from forms import UserLoginForm, UserCreateForm
from models import connect_db, User, AuthToken
from utils import get_hash_password
import uuid

router = APIRouter()


@router.get('/')
def index():
    return {"message": "Hello World"}


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
    return {'new_token_id': new_token.token}


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
    return user
