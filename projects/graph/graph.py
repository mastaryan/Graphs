from util import Stack, Queue  # These may come in handy

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print(f'Vertices must be valid')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        q.enqueue(starting_vertex)

        visited = [False] * len(self.vertices)
        visited[starting_vertex - 1] = True

        while q.size() > 0:
            vertex = q.dequeue()
            neighbors = self.get_neighbors(vertex)
            print(vertex)

            for v in neighbors:
                if visited[v - 1] == False:
                    q.enqueue(v)
                    visited[v - 1] = True

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        s.push(starting_vertex)

        visited = [False] * len(self.vertices)

        while s.size() > 0:
            vertex = s.pop()
            neighbors = self.get_neighbors(vertex)

            if not visited[vertex - 1]:
                print(vertex)
                visited[vertex - 1] = True

            for v in neighbors:
                if not visited[v - 1]:
                    s.push(v)

    def dft_recursive(self, starting_vertex, visited = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex using recursion.
        """
        if visited is None:
            visited = [False] * len(self.vertices)
        
        visited[starting_vertex - 1] = True
        print(starting_vertex)

        neighbors = self.get_neighbors(starting_vertex)

        for v in neighbors:
            if not visited[v - 1]:
                self.dft_recursive(v, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        q.enqueue([starting_vertex])

        while q.size() > 0:
            path = q.dequeue()
            vertex = path[-1]
            neighbors = self.get_neighbors(vertex)

            if vertex == destination_vertex:
                return path

            for v in neighbors:
                path_copy = path.copy()
                path_copy.append(v)
                q.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])

        while s.size() > 0:
            path = s.pop()
            vertex = path[-1]
            neighbors = self.get_neighbors(vertex)

            if vertex == destination_vertex:
                return path

            for v in neighbors:
                path_copy = path.copy()
                path_copy.append(v)
                s.push(path_copy)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited = None, path = []):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order using recursion.
        """
        if visited is None:
            visited = [False] * len(self.vertices)
        
        path_copy = path.copy()
        path_copy.append(starting_vertex)

        if starting_vertex == destination_vertex:
            return path_copy

        neighbors = self.get_neighbors(starting_vertex)
        for v in neighbors:
            if not visited[v - 1]:
                visited[v - 1] = True
                path_copy = self.dfs_recursive(v, destination_vertex, visited, path_copy)

                if path_copy[-1] == destination_vertex:
                    return path_copy
        
        return path

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    print('BFT')
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print('DFT Iterative')
    graph.dft(1)
    print('DFT Recursive')
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print('BFS')
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print('DFS Iterative')
    print(graph.dfs(1, 6))
    print('DFS Recursive')
    print(graph.dfs_recursive(1, 6))