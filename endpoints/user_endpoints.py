from fastapi import APIRouter, HTTPException, Security, security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND
from auth.auth import AuthHandler

from db.db import session
from models.user_models import UserInput, User, UserLogin
from repos.user_repos import find_user, select_all_users

user_router = APIRouter()
auth_handler = AuthHandler()



@user_router.post('/registration', status_code=201, tags=['users'],
                  description='Register new user')
def register(user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hashed_pwd, email=user.email,
             is_seller=user.is_seller)
    session.add(u)
    session.commit()
    return JSONResponse('Success', status_code=201)

@user_router.post('/login', tags=['users'])
def login(user: UserLogin):
    user_found = find_user(user.username)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid usename and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid usename and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}