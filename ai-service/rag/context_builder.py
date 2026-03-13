def build_llm_context(grouped_chunks, max_chars=16000):
    context_parts = []
    total_chars = 0

    for path, chunks in grouped_chunks.items():
        file_block = f"\nFILE: {path}\n```code\n"

        chunks = sorted(
            chunks,
            key=lambda c: (c.get('symbol') is None, c['start_line'])
        )

        for c in chunks:
            symbol_line = ""
            if c.get('symbol'):
                symbol_line = f"SYMBOL: {c['symbol']}\n"
            code_block = (
                f"\n{symbol_line}"
                f"// lines {c['start_line']}-{c['end_line']}\n"
                f"{c['content']}\n"
            )
            if total_chars+len(code_block) > max_chars:
                file_block+="\n```"
                context_parts.append(file_block)
                return "\n".join(context_parts)
            
            file_block+=code_block
            total_chars+=len(code_block)
        
        file_block+="\n```"
        context_parts.append(file_block)
    return "\n".join(context_parts)
