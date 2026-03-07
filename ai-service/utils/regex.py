import re

TOKEN_PATTERN = re.compile(r"\w+")

IMPORT_PATTERNS = {
    "python": [
        re.compile(r"import\s+([a-zA-Z0-9_\.]+)"),
        re.compile(r"from\s+([a-zA-Z0-9_\.]+)\s+import")
    ],
    "javascript": [
        re.compile(r'import\s+.*?\s+from\s+["\'](.*?)["\']'),
        re.compile(r'import\s+["\'](.*?)["\']'),
        re.compile(r'require\(["\'](.*?)["\']\)')
    ],
    "typescript": [
        re.compile(r'import\s+.*?\s+from\s+["\'](.*?)["\']'),
        re.compile(r'import\s+["\'](.*?)["\']'),
        re.compile(r'require\(["\'](.*?)["\']\)')
    ],
    "java": [
        re.compile(r'import\s+([a-zA-Z0-9_.]+);')
    ],
    "go": [
        re.compile(r'import\s+"([^"]+)"')
    ],
    "rust": [
        re.compile(r'use\s+([a-zA-Z0-9_:]+)')
    ]
}

SYMBOL_PATTERNS = {
    "python": [
        re.compile(r"def\s+([A-Za-z_]\w*)"),
        re.compile(r"class\s+([A-Za-z_]\w*)")
    ],
    "javascript": [
        re.compile(r"function\s+([A-Za-z_]\w*)"),
        re.compile(r"class\s+([A-Za-z_]\w*)"),
        re.compile(r"const\s+([A-Za-z_]\w*)\s*=\s*\("),
        re.compile(r"export\s+const\s+([A-Za-z_]\w*)")
    ],
    "typescript": [
        re.compile(r"function\s+([A-Za-z_]\w*)"),
        re.compile(r"class\s+([A-Za-z_]\w*)"),
        re.compile(r"const\s+([A-Za-z_]\w*)\s*=\s*\("),
        re.compile(r"export\s+const\s+([A-Za-z_]\w*)")
    ],
    "java": [
        re.compile(r"class\s+([A-Za-z_]\w*)"),
        re.compile(r"(?:public|private|protected)?\s*\w+\s+([A-Za-z_]\w*)\s*\(")
    ],
    "go": [
        re.compile(r"func\s+([A-Za-z_]\w*)"),
        re.compile(r"type\s+([A-Za-z_]\w*)\s+struct")
    ],
    "rust": [
        re.compile(r"fn\s+([A-Za-z_]\w*)"),
        re.compile(r"struct\s+([A-Za-z_]\w*)")
    ]
}

# called per chunk
def extract_symbol(content, language):
    patterns = SYMBOL_PATTERNS.get(language, [])
    
    # scanning only top of chunk (symbols usually live there)
    header = "\n".join(content.split("\n")[:20])
    
    for pattern in patterns:
        m = pattern.search(header)
        if m:
            return m.group(1)
    return None

# called per file
def extract_imports(content:str, language:str):
    imports = set()

    patterns = IMPORT_PATTERNS.get(language, [])

    # scanning only top of file (imports usually live there)
    header = "\n".join(content.split("\n")[:80])

    for pattern in patterns:
        matches = pattern.findall(header)
        imports.update(matches)

    return list(imports)