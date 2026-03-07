MAX_TOKEN = 12000
K_RRF = 60

RETRIEVAL_CONFIG = {
    "analysis": {
        "dense_k": 40,
        "sparse_k": 40,
        "window": 2,
        "graph_depth": 2,
        "rerank_top": 20
    },
    "plan": {
        "dense_k": 25,
        "sparse_k": 25,
        "window": 1,
        "graph_depth": 1,
        "rerank_top": 10
    },
    "patch": {
        "dense_k": 10,
        "sparse_k": 10,
        "window": 1,
        "graph_depth": 0,
        "rerank_top": 6
    }
}