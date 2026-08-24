from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db import *
from models import *
from  routers.auth import router as auth_router
from routers.users import router as user_router
from routers.club import router as club_router
from routers.activity import router as activity_router

from core.exceptions import AppException
from core.response import response_json


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=response_json(
            status_code=exc.status_code,
            message=exc.message,
            error=exc.error,
            path=request.url.path
        )
    )

@app.get("/health")
def health_check():
    return response_json(
        status_code=200,
        message="Server is running",
        data={
            "status": "OK"
        }
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(club_router)
app.include_router(activity_router)