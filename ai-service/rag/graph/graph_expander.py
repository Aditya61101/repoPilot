
def expand_graph(files, repo_graph, limit=3):
    expanded = set(files)
    added = 0
    for f in files:
        if f not in repo_graph:
            continue
        imports = repo_graph.get(f,{}).get('imports',[])
        for imp in imports[:limit]:
            if added >= limit:
                return list(expanded)
            for candidate in repo_graph.keys():
                if imp in candidate and candidate not in expanded:
                    expanded.add(candidate)
                    added+=1
                    break
    return list(expanded)