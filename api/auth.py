from fastapi import FastAPI, HTTPException, Depends, status, Response, APIRouter
from sqlalchemy.orm import Session





from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


from .schemas import CreateUser
from .models import User
from .database import engine, SessionLocal, get_db

router = APIRouter(prefix='/auth', tags=['authorization'])


SECRET_KEY = 'qddgthji134566uu7y54rg789lp09ht553gy77ij8433g'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')




@router.post('/user')
def create_user(user:CreateUser, db:Session=Depends(get_db)):
    db_result = User(username=user.username, hashed_password=bcrypt_context.hash(user.password))
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


@router.post('/token')
def login_for_access_token(data=Depends(OAuth2PasswordRequestForm), db:Session=Depends(get_db)):
    user = authenticate_user(data.username, data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    token = create_access_token(user.username, user.id)

    return {"access_token": token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    return user

def create_access_token(username: str, user_id: int):
    encode = {'sub': username, 'id': user_id}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {'username':username, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    

