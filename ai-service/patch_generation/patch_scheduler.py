import networkx as nx

def schedule_patch_plan(patch_plan, repo_graph):
    G = nx.DiGraph()
    
    id_to_step = {}
    file_to_id = {}

    # adding nodes
    for step in patch_plan:
        step_id = step['id']
        file_path = step['file']

        id_to_step[step_id] = step
        file_to_id[file_path] = step_id
        
        G.add_node(step_id)
    
    # planner dependencies(primary)
    for step in patch_plan:
        step_id = step['id']
        for dep in step.get("depends_on", []):
            if dep not in id_to_step:
                raise ValueError()
            
            G.add_edge(dep, step_id)
    
    # repo_graph structural dependencies
    for a in patch_plan:
        file_a = a['file']
        id_a = a['id']
        for b in patch_plan:
            if a is b:
                continue

            file_b = b['file']
            id_b = b['id']

            # static dependency
            if repo_graph.has_edge(file_a, file_b):
                if not nx.has_path(G, id_a, id_b) and not G.has_edge(id_b,id_a):
                    G.add_edge(id_b,id_a)
            # reverse dependency
            elif repo_graph.has_edge(file_b, file_a):
                if not nx.has_path(G, id_b, id_a) and not G.has_edge(id_a,id_b):
                    G.add_edge(id_a,id_b)
    # SCC
    C = nx.condensation(G)

    generations = list(nx.topological_generations(C))
    
    batches = []
    for gen in generations:
        batch = []
        for scc_node in gen:
            members = C.nodes[scc_node]['members']
            for step_id in members:
                batch.append(id_to_step[step_id])

        batches.append(batch)
    return batches
