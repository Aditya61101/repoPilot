from fastapi import FastAPI
from api.routes import router as ai_router

app = FastAPI()

app.include_router(ai_router)