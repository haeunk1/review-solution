from fastapi import FastAPI
from app.api.v1 import  reviews, hospitals

app = FastAPI(title="Review AI Solution")

# API 라우터 등록
#app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["hospitals"])
@app.get("/")
def root():
    return {"message": "Welcome to Place-AI API"}