from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import models
from .core import database
from .routers.api import api_router
from .core.static import SPAStaticFiles
from pathlib import Path
from contextlib import asynccontextmanager

baseDir = Path(__file__).resolve().parent.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api_router)

app.mount('/', SPAStaticFiles(directory=f'{baseDir}/frontend/', html=True), name='frontend')