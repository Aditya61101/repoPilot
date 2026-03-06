import os
# from transformers import logging
from sentence_transformers import SentenceTransformer

os.environ['HF_HUB_OFFLINE'] = "1"
os.environ['TRANSFORMERS_OFFLINE'] = "1"

model = SentenceTransformer("BAAI/bge-small-en", device='cpu')

def embed_texts(texts):
    return model.encode(texts, batch_size=32, show_progress_bar=False)

def embed_query(text):
    return model.encode([text])

# def create_embeddings():
#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
#     return embeddings