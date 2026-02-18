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


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    #Version inicial de DFS

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



def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """

    #Version inicial BFS

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



def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    #Version inicial UCS

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




def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    #Version inicial A*
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


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
