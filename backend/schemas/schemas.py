from pydantic import BaseModel, ConfigDict, field_validator, Field, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from ..core.enums import WeekDays

class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=6)]
    password: str = Field(min_length=6)
    
class UserLogin(BaseModel):
    username: str
    password: str
    
class TaskCreate(BaseModel):
    task_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
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
    
class TaskListResponse(BaseModel):
    user_id: int
    data: list[TaskResponse]
    
class CompletionListResponse(BaseModel):
    user_id: int
    data: list[CompletionResponse]