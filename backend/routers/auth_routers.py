from fastapi import APIRouter, Depends, HTTPException
from ..schemas import schemas
from ..core import database
from ..services import auth, crud
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import psycopg2

router = APIRouter(prefix='/api', tags=['Users', 'Auth'])

@router.post('/users/')
def createUser(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        if user.username and user.password != '':
            hashPassword = auth.hashPassword(user.password)
            data = crud.createUser({'username': user.username, 'password': hashPassword}, db)
        else:
            raise HTTPException(status_code=400, detail='Todos os campos devem ser preenchidos.')
    except IntegrityError as e:
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            raise HTTPException(status_code=400, detail='Já existe um usuário com esse nome.')
        else:
            raise HTTPException(status_code=500, detail=f'Erro ao criar usuário: {e}')
    return {'data': data}

@router.post('/login/')
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    row = crud.searchData(user.username, db)
    if row is not None:
        test = auth.verifyPassword(user.password, row.password)
        if test:
            token = auth.createToken({'sub': user.username})
            return {'access_token': token, 'token_type': 'bearer'}
        else:
            raise HTTPException(status_code=401, detail='Usuário ou senha incorretos.')
    else:
        raise HTTPException(status_code=401, detail='Usuário ou senha incorretos.')