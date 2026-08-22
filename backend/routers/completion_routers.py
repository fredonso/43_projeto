from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import schemas
from ..core import database
from ..services import crud, auth
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

router = APIRouter(prefix='/api/tasks', tags=['Completions'])

@router.post('/{taskId}/completions/', response_model=schemas.CompletionResponse, status_code=status.HTTP_201_CREATED)
def createCompletion(completion: schemas.CompletionCreate, taskId: int, user = Depends(auth.currentUser), db: Session = Depends(database.get_db)):
    userId = user.id
    try:
        data = crud.createCompletion(completion, taskId, userId, db)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não existe uma tarefa com esse ID.')
        return {
            'user_id': userId,
            'task_id': taskId,
            'completed_at': data.completed_at
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ocorreu um erro inesperado. Tente novamente mais tarde. {e}')
    
@router.get('/completions/{date}/', response_model=schemas.CompletionListResponse, status_code=status.HTTP_200_OK)
def listCompletions(date: date, user = Depends(auth.currentUser), db: Session = Depends(database.get_db)):
    userId = user.id
    data = crud.listCompletions(date, userId, db)
    return {
        'user_id': userId,
        'data': data
    } 