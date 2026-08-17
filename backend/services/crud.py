from ..models import models
from datetime import datetime
from sqlalchemy import cast, Date

def searchData(user, db):
    return db.query(models.User).filter(models.User.username == user).first()

def createUser(user, db):
    newUser = models.User(username=user['username'], password=user['password'])
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser.username

def createTasks(task, userId, db):
    newTask = models.Task(
        user_id=userId, 
        task_name=task['taskName'], 
        task_description=task['taskDescription'], 
        days=[models.Day(day=d) for d in task['taskDays']]
        )
    db.add(newTask)
    db.commit()
    db.refresh(newTask)
    return newTask

def listTasks(userId, db):
    return db.query(models.Task).filter(models.Task.user_id == userId).all()

def deleteTask(taskId, userId, db):
    deletedTask = db.query(models.Task).filter(models.Task.user_id == userId, models.Task.id == taskId).first()
    if deletedTask:
        db.delete(deletedTask)
        db.commit()
    return deletedTask

def updateTask(task, taskId, userId, db):
    updatedTask = db.query(models.Task).filter(models.Task.user_id == userId, models.Task.id == taskId).first()
    if updatedTask:
        updatedTask.task_name = task['taskName']
        updatedTask.task_description = task['taskDescription']
        updatedTask.days = [models.Day(day=d) for d in task['taskDays']]
        db.commit()
        db.refresh(updatedTask)
    return updatedTask

def createCompletion(date, taskId, userId, db):
    newCompletion = models.Completion(
        user_id = userId,
        task_id = taskId,
        completed_at = datetime.fromisoformat(date)
    )
    db.add(newCompletion)
    db.commit()
    db.refresh(newCompletion)
    return newCompletion

def listCompletions(date, userId, db):
    return db.query(models.Completion).filter(models.Completion.user_id == userId, cast(models.Completion.completed_at, Date) == date).all()