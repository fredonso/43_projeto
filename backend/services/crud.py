from ..models import models
from datetime import datetime

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
        task_name=task.task_name, 
        task_description=task.task_description, 
        days=[models.Day(day=d) for d in task.days]
        )
    db.add(newTask)
    db.commit()
    db.refresh(newTask)
    return newTask

def listTasks(userId, db):
    return db.query(models.Task).filter(models.Task.user_id == userId).all()

def deleteTask(taskId, userId, db):
    verifyTask = db.query(models.Task).filter(models.Task.user_id == userId, models.Task.id == taskId).first()
    if not verifyTask:
        return None
    db.delete(verifyTask)
    db.commit()
    return verifyTask

def updateTask(task, taskId, userId, db):
    verifyTask = db.query(models.Task).filter(models.Task.user_id == userId, models.Task.id == taskId).first()
    if not verifyTask:
        return None
    verifyTask.task_name = task.task_name
    verifyTask.task_description = task.task_description
    verifyTask.days = [models.Day(day=d) for d in task.days]
    db.commit()
    db.refresh(verifyTask)
    return verifyTask

def createCompletion(date, taskId, userId, db):
    verifyTask = db.query(models.Task).filter(models.Task.user_id == userId, models.Task.id == taskId).first()
    if not verifyTask:
        return None
    newCompletion = models.Completion(
        user_id = userId,
        task_id = taskId,
        completed_at = date.completed_at
    )
    db.add(newCompletion)
    db.commit()
    db.refresh(newCompletion)
    return newCompletion

def listCompletions(date, userId, db):
    beginning = datetime.combine(date,datetime.min.time())
    end = datetime.combine(date, datetime.max.time())
    return db.query(models.Completion).filter(models.Completion.user_id == userId, models.Completion.completed_at.between(beginning, end)).all()