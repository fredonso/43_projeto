from fastapi import APIRouter
from .auth_routers import router as authRouter
from .completion_routers import router as completionRouter
from .task_routers import router as taskRouter

api_router = APIRouter()

api_router.include_router(authRouter)
api_router.include_router(completionRouter)
api_router.include_router(taskRouter)