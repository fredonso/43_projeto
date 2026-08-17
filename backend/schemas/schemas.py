from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from ..core.enums import WeekDays

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str
    
class TaskCreate(BaseModel):
    task_name: str
    task_description: str | None
    days: list[WeekDays]

class TaskResponse(BaseModel):
    user_id: int
    id: int
    task_name: str
    task_description: str | None
    days: list[WeekDays]
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('days', mode='before')
    @classmethod
    def enumExtractor(cls, value: list) -> list:
        return [item.day for item in value]
 
class CompletionCreate(BaseModel):
    completed_at: datetime
    
class CompletionResponse(BaseModel):
    user_id: int
    task_id: int
    completed_at: datetime
    
    model_config = ConfigDict(from_attributes=True)