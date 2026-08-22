from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import schemas
from ..core import database
from ..services import auth, crud
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix='/api', tags=['Tasks'])

@router.post('/tasks/', response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def createTask(task: schemas.TaskCreate, user = Depends(auth.currentUser), db: Session = Depends(database.get_db)):
    userId = user.id
    try:
        data = crud.createTasks(task, userId, db)
        return {
            'user_id': userId,
            'id': data.id,
            'task_name': data.task_name,
            'task_description': data.task_description,
            'days': data.days
            }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ocorreu um erro inesperado. Tente novamente mais tarde.')
    
@router.get('/tasks/', response_model=schemas.TaskListResponse, status_code=status.HTTP_200_OK)
def listTasks(user = Depends(auth.currentUser), db: Session = Depends(database.get_db)):
    userId = user.id
    data = crud.listTasks(userId, db)
    return {
        'user_id': userId,
        'data': data
    }
    
@router.delete('/tasks/{taskId}/', status_code=status.HTTP_204_NO_CONTENT)
def deleteTask(taskId: int, user = Depends(auth.currentUser), db: Session = Depends(database.get_db)):
    userId = user.id
    try:
        deleted = crud.deleteTask(taskId, userId, db)
        if deleted is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não existe uma tarefa com esse ID.')
        return
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ocorreu um erro inesperado. Tente novamente mais tarde.')
    
@router.put('/tasks/{taskId}/', response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
def updateTask(task: schemas.TaskCreate, taskId: int, user = Depends(auth.currentUser), db: Session = Depends(database.get_db)):
    userId = user.id
    try:
        updated = crud.updateTask(task, taskId, userId, db)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não existe uma tarefa com esse ID.')
        return {
            'user_id': userId,
            'id': taskId,
            'task_name': updated.task_name,
            'task_description': updated.task_description,
            'days': updated.days
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ocorreu um erro inesperado. Tente novamente mais tarde.')
