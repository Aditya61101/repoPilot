from collections import defaultdict
from rag.graph.import_resolver import resolve_import

def build_repo_graph(chunks, file_index, module_index):
    graph = defaultdict(lambda: {
        "imports": set(),
        "imported_by": set(),
        "symbols": set()
    })
    for chunk in chunks:
        path = chunk['path']
        symbol = chunk.get('symbol')
        imports = chunk.get('imports', [])

        if symbol:
            graph[path]['symbols'].add(symbol)
        
        for imp in imports:
            resolved = resolve_import(
                imp,
                path, 
                file_index, 
                module_index
            )
            if resolved:
                graph[path]['imports'].add(resolved)
                graph[resolved]['imported_by'].add(path)

    # converting set to list, important for serialization
    repo_graph = {}
    for p, d in graph.items():
        repo_graph[p] = {
            "imports": list(d['imports']),
            "imported_by": list(d['imported_by']),
            "symbols": list(d['symbols']),
        }
    return repo_graph