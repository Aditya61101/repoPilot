from utils.regex import SYMBOL_PATTERNS

MAX_CHUNK_LINES = 200
MIN_SYMBOLS = 2

def build_line_index(content):
    line_starts = [0]
    for i, c in enumerate(content):
        if c == "\n":
            line_starts.append(i + 1)
    return line_starts


def char_to_line(pos, line_index):
    import bisect
    return bisect.bisect_right(line_index, pos)


def split_by_symbols(path, content, lang):

    patterns = SYMBOL_PATTERNS.get(lang)
    if not patterns:
        return None

    symbol_map = {}

    for pattern in patterns:
        for m in pattern.finditer(content):
            symbol_map[m.start()] = m.group(1)

    if len(symbol_map) < MIN_SYMBOLS:
        return None

    matches = sorted(symbol_map.items())

    line_index = build_line_index(content)
    lines = content.splitlines()

    chunks = []

    for i, (pos, symbol) in enumerate(matches):

        start_line = char_to_line(pos, line_index)

        if i + 1 < len(matches):
            end_pos = matches[i+1][0]
        else:
            end_pos = len(content)

        end_line = char_to_line(end_pos, line_index)

        if end_line - start_line > MAX_CHUNK_LINES:
            return None

        chunk_text = "\n".join(lines[start_line-1:end_line])

        chunks.append({
            "chunk_id": f"{path}:{start_line}-{end_line}",
            "path": path,
            "language": lang,
            "symbol": symbol,
            "start_line": start_line,
            "end_line": end_line,
            "content": chunk_text
        })

    return chunks if chunks else None