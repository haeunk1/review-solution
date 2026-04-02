from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import reviews, stores, analysis, replies
from app.services.scheduler_service import init_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시
    init_scheduler()
    yield
    # 앱 종료 시
    stop_scheduler()


app = FastAPI(title="Review AI Solution", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(stores.router, prefix="/api/v1/stores", tags=["stores"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(replies.router, prefix="/api/v1/replies", tags=["replies"])


@app.get("/")
def root():
    return {"message": "Welcome to Review AI Solution API"}
