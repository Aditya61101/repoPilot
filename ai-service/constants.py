import os

MAX_TOKEN = 12000
K_RRF = 60
MAX_GENERATOR_CONTEXT_CHARS = 12000

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

# Language-specific syntax check commands
SYNTAX_CHECKERS = {
    ".py": ["python", "-m", "py_compile"],
    ".js": ["node", "--check"],
    ".jsx": ["node", "--check"],
    ".sh": ["bash", "-n"],
}

EXTENSION_MAPPING = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".cpp": "cpp",
    ".c": "cpp",
    ".rs": "rust",
    ".html": "html",
    ".css": "css"
}