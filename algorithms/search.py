from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyHouseSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyHouse. For any other building, the
    sequence of moves will be incorrect, so only use this for tinyHouse.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def _reconstruct_path(parents, initial_state, goal_state):
    """Recorre el diccionario de padres desde goal hasta initial y devuelve la lista de acciones."""
    path = []
    state = goal_state
    while state != initial_state:
        parent, action = parents[state]
        path.append(action)
        state = parent
    path.reverse()
    return path

def depthFirstSearch(problem: SearchProblem):
    """

    Version inicial de DFS implementación autonoma: 

    
    #Creamos visitados, la pila y una estructrua para almacenar los padres
    visited=set()
    stack=utils.Stack()
    parents={}

    initial_state=problem.getStartState()
    stack.push(initial_state)
    #Se itera mientras no este vacia
    while not stack.isEmpty(): 
        current=stack.pop()
        #Si se encuentra el estado objetivo se reconstruye el camino, se revierte y se devuelve
        if problem.isGoalState(current):
            path=[]
            state=current
            while state != initial_state: 
                parent, action = parents[state]
                path.append(action)
                state=parent
            path.reverse()
            return path
    #Si no ha sido visitado, se marca y se agregan los sucesores a la pila y se guarda en la estructura para almacenar la ruta padre-hijo
        if current not in visited: 
            visited.add(current)
            for node,action,cost in problem.getSuccessors(current):
                if node not in visited:
                    parents[node]= (current,action) 
                    stack.push(node)
    return []
    
    """
    #Version Optimizada con IA

    #Creamos visitados, la pila y una estructrua para almacenar los padres
    visited = set()
    stack = utils.Stack()
    parents = {}

    initial_state = problem.getStartState()
    stack.push(initial_state)

    while not stack.isEmpty():
        current = stack.pop()

        # Verificar objetivo ANTES de marcar visitado para no perder estados
        if problem.isGoalState(current):
            return _reconstruct_path(parents, initial_state, current)

        if current not in visited:
            visited.add(current)
            for node, action, cost in problem.getSuccessors(current):
                if node not in visited:
                    parents[node] = (current, action)
                    stack.push(node)

    return []



def breadthFirstSearch(problem: SearchProblem):
    """
    Version inicial de BFS implementación autonoma: 

    visited=set()
    queue=utils.Queue()
    parents={}

    initial_state=problem.getStartState()
    visited.add(initial_state)
    queue.push(initial_state)

    #Se itera mientras no este vacia
    while not queue.isEmpty(): 
        current=queue.pop()
        #Si se encuentra el estado objetivo se reconstruye el camino, se revierte y se devuelve
        if problem.isGoalState(current):
            path=[]
            state=current
            while state != initial_state: 
                parent, action = parents[state]
                path.append(action)
                state=parent
            path.reverse()
            return path
    #Se marca y se agregan los sucesores a la fila y se guarda en la estructura para almacenar la ruta padre-hijo
        for node,action,cost in problem.getSuccessors(current):
            if node not in visited:
                visited.add(node)
                parents[node]= (current,action) 
                queue.push(node)
    return []

    """

    #Version Optimizada con IA

    visited = set()
    queue = utils.Queue()
    parents = {}

    initial_state = problem.getStartState()

    # Verificación temprana si el inicio ya es meta
    if problem.isGoalState(initial_state):
        return []

    visited.add(initial_state)
    queue.push(initial_state)

    while not queue.isEmpty():
        current = queue.pop()

        for node, action, cost in problem.getSuccessors(current):
            if node not in visited:
                parents[node] = (current, action)

                # Early exit: verificar al encolar evita expandir un nivel extra
                if problem.isGoalState(node):
                    return _reconstruct_path(parents, initial_state, node)

                visited.add(node)
                queue.push(node)

    return []



def uniformCostSearch(problem: SearchProblem):
    """

    Version inicial de UCS implementación autonoma:

    visited=set()
    queue=utils.PriorityQueue()
    parents={}

    initial_state=problem.getStartState()
    costs={initial_state:0} #Utilizamos una estructura de costos para saber cual es el menor costo que he encontrado
    queue.push(initial_state,0)

    while not queue.isEmpty():

        current= queue.pop()
        #Si se encuentra el estado objetivo despues de sacar de la cola de prioridad, se reconstruye el camino y se retorna
        if problem.isGoalState(current):
            path=[]
            state=current
            while state != initial_state: 
                parent, action = parents[state]
                path.append(action)
                state=parent
            path.reverse()
            return path
        #Si el actual no esta visitado, lo marco y miro sus sucesores
        if current not in visited: 
            visited.add(current)
            for node,action,cost in problem.getSuccessors(current):
                new_cost=costs[current] + cost
                if node not in visited and (node not in costs or costs[node]> new_cost): #Solo modifico los costos de los sucesores si no han sido visitados o si hay un costo menor al que ya habia encontrado
                    costs[node]=new_cost
                    parents[node]= (current,action) 
                    queue.update(node,new_cost)
    return []


    """
    #Version Optimizada con IA

    visited = set()
    queue = utils.PriorityQueue()
    parents = {}

    initial_state = problem.getStartState()
    costs = {initial_state: 0}
    queue.push(initial_state, 0)

    while not queue.isEmpty():
        current = queue.pop()

        # Verificar goal al desencolar garantiza optimalidad en UCS
        if problem.isGoalState(current):
            return _reconstruct_path(parents, initial_state, current)

        if current not in visited:
            visited.add(current)
            for node, action, cost in problem.getSuccessors(current):
                new_cost = costs[current] + cost
                if node not in visited and (node not in costs or costs[node] > new_cost):
                    costs[node] = new_cost
                    parents[node] = (current, action)
                    queue.update(node, new_cost)

    return []




def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Version inicial de A* implementación autonoma:

     visited=set()
    queue=utils.PriorityQueue()
    parents={}

    initial_state=problem.getStartState()
    costs={initial_state:0}
    queue.push(initial_state,heuristic(initial_state,problem))

    while not queue.isEmpty():
        current= queue.pop()
        if problem.isGoalState(current): #Evaluar una vez sacamos de pila
            path=[]
            state=current
            while state != initial_state: 
                parent, action = parents[state]
                path.append(action)
                state=parent
            path.reverse()
            return path
        
        if current not in visited: 
            visited.add(current)
            for node,action,cost in problem.getSuccessors(current):
                new_cost=costs[current] + cost
                if node not in visited and (node not in costs or costs[node]> new_cost):
                    costs[node]=new_cost
                    parents[node]= (current,action) 
                    queue.update(node,new_cost + heuristic(node,problem))
    return []

    """
    #Version optimizada con IA
    visited = set()
    queue = utils.PriorityQueue()
    parents = {}

    initial_state = problem.getStartState()
    costs = {initial_state: 0}
    queue.push(initial_state, heuristic(initial_state, problem))

    while not queue.isEmpty():
        current = queue.pop()

        # Verificar goal al desencolar garantiza optimalidad (heurística admisible)
        if problem.isGoalState(current):
            return _reconstruct_path(parents, initial_state, current)

        if current not in visited:
            visited.add(current)
            for node, action, cost in problem.getSuccessors(current):
                new_cost = costs[current] + cost
                if node not in visited and (node not in costs or costs[node] > new_cost):
                    costs[node] = new_cost
                    parents[node] = (current, action)
                    queue.update(node, new_cost + heuristic(node, problem))

    return []


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
