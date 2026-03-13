from collections import defaultdict

def expand_graph(files, repo_graph, depth=2, max_files=20):
    scores = defaultdict(float)

    frontier = [(f, 1.0, 0) for f in files]
    while frontier:
        file, score, dist = frontier.pop(0)

        if dist > depth:
            continue
        
        scores[file]+=score
        
        if file not in repo_graph:
            continue
        
        # dependencies (imports)
        for dep in repo_graph.successors(file):
            new_score = score*0.8
            frontier.append((dep, new_score, dist+1))

        # dependents (imported_by)
        for user in repo_graph.predecessors(file):
            new_score = score*0.6
            frontier.append((user, new_score, dist+1))

    ranked = sorted(scores.items(), key=lambda x:x[1], reverse=True)

    expanded = [f for f,_ in ranked[:max_files]]
    
    return expanded