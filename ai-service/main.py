from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as ai_router
from rag.models import get_reranker

app = FastAPI()

@app.on_event('startup')
def load_models():
    get_reranker()

app.include_router(ai_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)