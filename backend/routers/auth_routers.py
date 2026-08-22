from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import schemas
from ..core import database
from ..services import auth, crud
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import psycopg2

router = APIRouter(prefix='/api', tags=['Auth'])

@router.post('/users/', status_code=status.HTTP_201_CREATED)
def createUser(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Todos os campos devem ser preenchidos.')
    hashPassword = auth.hashPassword(user.password)
    try:
        data = crud.createUser({'username': user.username, 'password': hashPassword}, db)
        return {'data': data}
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um usuário com esse nome.')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ocorreu um erro inesperado. Tente novamente mais tarde.')

@router.post('/login/', status_code=status.HTTP_200_OK)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    row = crud.searchData(user.username, db)
    if row is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário ou senha incorretos.')
    if not auth.verifyPassword(user.password, row.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário ou senha incorretos.')
    token = auth.createToken({'sub': user.username})
    return {'access_token': token, 'token_type': 'bearer'}        