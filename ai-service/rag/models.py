from sentence_transformers import CrossEncoder

reranker = None
def get_reranker():
    global reranker
    if reranker is None:
        reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            max_length=512,
            device='cpu'
        )
    return reranker