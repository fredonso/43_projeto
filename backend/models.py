from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base
from .enums import WeekDays
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False, index=True)
    tasks = relationship('Task', back_populates='user')
    completions = relationship('Completion', back_populates='user')
    
class Task(Base):
    __tablename__ = 'tasks'
    
    user_id = Column(Integer, ForeignKey('users.id'))
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False, index=True)
    task_description = Column(String, index=True)
    user = relationship('User', back_populates='tasks')
    days = relationship('Day', back_populates='tasks')
    completions = relationship('Completion', back_populates='tasks')

class Day(Base):
    __tablename__ = 'task_days'
    
    task_id = Column(Integer, ForeignKey('tasks.id'))
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Enum(WeekDays), index=True)
    tasks = relationship('Task', back_populates='days')
    
class Completion(Base):
    __tablename__ = 'completions'
    
    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    id = Column(Integer, primary_key=True, index=True)
    completed_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    user = relationship('User', back_populates='completions')
    tasks = relationship('Task', back_populates='completions')