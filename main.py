import sys
from math import sqrt


class Node:
    '''
    El nodo de un grafo
    name: (string) Nombre del nodo
    visited: (bool) Si el nodo ha sido visitado
    color: () Un identificador, puede ser un bool, string o int
    adj_list: Lista de nodos adjacentes
    '''

    def __init__(self, name, visited = False, color = 0):
        self.name = name
        self.visited = visited
        self.color = color
        self.adj_list = []

    def __str__(self):
        ''' Lo que se imprime al hacer print(Nodo('x')) '''
        return "Node: {} | Color: {} | Visited: {}\nAdj Nodes: {}\n".format(self.name, self.color, self.visited, [i.name for i in self.adj_list])

    def set_color(self, col):
        ''' Setea un color para el nodo '''
        self.color = col

    def get_color(self):
        ''' Devuelve el color del nodo '''
        return self.color

    def mark_visited(self):
        ''' Marca como visitado al nodo '''
        self.visited = True

    def mark_unvisited(self):
        ''' Marca como NO visitado al nodo '''
        self.visited = False

    def is_visited(self):
        ''' Para verificar si el nodo ha sido visitado o no '''
        return self.visited

    def add_adj(self, node):
        ''' Agrega un nodo a la lista de nodos adjacentes del nodo actual '''
        self.adj_list.append(node)

    def get_adjs(self):
        ''' Devuelve la lista de nodos adyacente del nodo actual '''
        return self.adj_list


class Graph:
    ''' Modela el grafo, posee todos los nodos y resuelve el sudoku '''
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.soluciones = []

    @staticmethod
    def to_node(data):
        ''' Basado en la data recibida de un espacio del txt se crea un nodo '''
        if data != '':
            node = Node(int(data))
            if data != '0':
                node.set_color(int(data))
                node.mark_visited()
            return node
        else:
            raise Exception("Los espacios sin un numero deben ser llenados con ceros")

    def read_graph(self, file):
        ''' Lee y modela el grafo de un archivo '''
        # Leyendo grafo y creando Node's
        with open(file, 'r') as gf:
            graph_lines = gf.read().replace(' ', '').split('\n')
        graph = [list(map(self.to_node, x.split(','))) for x in graph_lines if x != '']

        # Verificando que el tamano sea un cuadrado perfecto
        g_len = len(graph)
        self.colors = set(range(1, g_len+1))
        if int(sqrt(g_len))**2 != g_len:
            raise Exception("Tamano no permitido para el sudoku")
        # Verificando que el sudoku sea cuadrado
        if sum([len(i) for i in graph]) != g_len**2:
            raise Exception("El sudoku debe ser cuadrado")

        # sg = Sub grid
        sg = sqrt(g_len)
        # Por cada nodo en el grafo se agregan como adycentes aquellos grafos que no pueden tener el mismo color
        for x0 in range(g_len):
            for y0 in range(g_len):
                for x1 in range(g_len):
                    for y1 in range(g_len):
                        if x0 != x1 or y0 != y1:    # Si el nodo es diferente a si mismo
                            # Si el nodo esta en la misma cuadricula o misma fila/columna
                            if (x0//sg == x1//sg and y0//sg == y1//sg) or (x0 == x1 or y0 == y1):
                                graph[x0][y0].add_adj(graph[x1][y1]) # Agregando nodo x1,y1 a lista de adyacentes de x0,y0
                self.nodes.append(graph[x0][y0])
        self.graph = graph

    def adj_colors(self, node):
        ''' Retorna los colores adyacentes a un nodo'''
        return set(i.get_color() for i in node.get_adjs())

    def solve(self):
        ''' Inicia la recursion para resolver el sudoku '''
        self.find_all(self.nodes)

    def find_all(self, nodes):
        ''' 
        Recorre los nodos con la menor cantidad de colores posibles
        e intenta las diferentes combinaciones de colores para esos nodos
        imprimiendo las posibles soluciones si existe alguna
        '''
        if all([i.get_color() for i in nodes]):
            print("POSIBLE SOLUCION")
            self.print_sudoku()
            #sys.exit(0) # Para salir al encontrar una solucion
        else:
            not_visited = [n for n in nodes if not n.is_visited()]
            to_color_node = min(not_visited, key=lambda x: len(self.colors - self.adj_colors(x)))
            possible_colors = self.colors-self.adj_colors(to_color_node)
            for col in possible_colors:
                to_color_node.set_color(col)
                to_color_node.mark_visited()
                self.find_all(nodes)
                to_color_node.set_color(0)
                to_color_node.mark_unvisited()

    def print_sudoku(self):
        ''' Imprime el sudoku '''
        for row in self.graph:
            for node in row:
                print(node.get_color(), end=' ')
            print()
        print()

    def print_graph(self):
        ''' Imprime el grafo '''
        for node in self.nodes:
            print(node)


if __name__ == '__main__':
    le_graph = Graph()
    le_graph.read_graph('sudoku.txt')
    print("SUDOKU INICIAL")
    le_graph.print_sudoku()
    le_graph.solve()
