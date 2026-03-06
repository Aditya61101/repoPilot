import os

def detect_language(path):
    ext = os.path.splitext(path)[1].lower()

    mapping = {
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

    return mapping.get(ext, "generic")