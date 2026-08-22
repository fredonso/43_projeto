import bcrypt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..core import database
from . import crud

httpBearer = HTTPBearer()
load_dotenv("SECRET_KEY.env")
secretKey = os.getenv("SECRET_KEY_HEX")
algorithm = "HS256"

def hashPassword(password: str) -> str:
    passwordBytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hash = bcrypt.hashpw(passwordBytes, salt)
    return hash.decode('utf-8')

def verifyPassword(password: str, hash: str) -> bool:
    passwordBytes = password.encode('utf-8')
    hashBytes = hash.encode('utf-8')
    return bcrypt.checkpw(passwordBytes, hashBytes)

def createToken(data: dict) -> str:
    codify = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    codify.update({"exp": expire})
    encodedJwt = jwt.encode(codify, secretKey, algorithm=algorithm)
    return encodedJwt

def validateToken(token: str) -> str:
    payload = jwt.decode(token, secretKey, algorithms=[algorithm])
    username: str = payload.get("sub")
    return username

def currentUser(auth: HTTPAuthorizationCredentials = Depends(httpBearer), db: Session = Depends(database.get_db)):
    token = auth.credentials
    error = HTTPException(status_code=401, detail='Não foi possível validar as credenciais', headers={"WWW-Authenticate": "Bearer"})
    try:
        username = validateToken(token)
        if not username:
            raise error
    except (jwt.ExpiredSignatureError, JWTError):
        raise error
    userData = crud.searchData(username, db)
    if not userData:
        raise HTTPException(status_code=401, detail='Usuário não encontrado.')
    return userData