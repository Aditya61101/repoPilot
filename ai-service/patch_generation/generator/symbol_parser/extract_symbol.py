from tree_sitter_languages import get_parser
from patch_generation.generator.symbol_parser.tree_sitter_parser import find_symbol_node
from utils.language_detection import detect_language

def extract_symbol_range_ts(file_content: str, symbol: str, language: str):

    # parser = get_ts_parser(language)
    print("language for symbol extraction: ", language)
    parser = get_parser(language)

    code_bytes = file_content.encode()

    tree = parser.parse(code_bytes)

    root = tree.root_node

    node = find_symbol_node(root, code_bytes, symbol)

    if not node:
        return None

    start_line = node.start_point[0] + 1
    end_line = node.end_point[0] + 1

    return start_line, end_line

def extract_symbol_range(repo_state, step):

    path = step["file"]
    
    symbol = step.get("symbol")
    if not symbol:
        return step['start_line'], step['end_line']

    language = detect_language(path)

    lines = repo_state[path]

    file_content = "\n".join(lines)

    if language:
        result = extract_symbol_range_ts(file_content, symbol, language)
        print("Extracted symbol range: ", result)
        if result:
            return result
    return step['start_line'], step['end_line']
    # fallback to regex
    # return extract_symbol_range_regex(repo_state, step)