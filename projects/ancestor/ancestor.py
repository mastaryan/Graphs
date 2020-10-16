def earliest_ancestor(ancestors, starting_node):
    ancestor_graph = {}
    
    for parent, child in ancestors:
        if child in ancestor_graph:
            ancestor_graph[child].add(parent)
        else:
            ancestor_graph[child] = set()
            ancestor_graph[child].add(parent)

    if starting_node not in ancestor_graph.keys():
        return -1
    
    current = starting_node
    parent = min(ancestor_graph[current])

    while parent in ancestor_graph.keys():
        current = parent
        parent = min(ancestor_graph[current])
    
    return parent