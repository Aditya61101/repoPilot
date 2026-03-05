from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en", device='cpu')

def embed_texts(texts):
    return model.encode(texts, batch_size=32, show_progress_bar=False)

def embed_query(text):
    return model.encode([text])

# def create_embeddings():
#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
#     return embeddings