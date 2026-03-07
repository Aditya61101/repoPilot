from fastapi import FastAPI
from api.routes import router as ai_router
from rag.models import get_reranker

app = FastAPI()

@app.on_event('startup')
def load_models():
    get_reranker()

app.include_router(ai_router)
