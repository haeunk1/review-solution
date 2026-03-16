from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import reviews, hospitals
from app.services.scheduler_service import init_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시
    init_scheduler()
    yield
    # 앱 종료 시
    stop_scheduler()


app = FastAPI(title="Review AI Solution", lifespan=lifespan)

# API 라우터 등록
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["hospitals"])


@app.get("/")
def root():
    return {"message": "Welcome to Review AI Solution API"}
