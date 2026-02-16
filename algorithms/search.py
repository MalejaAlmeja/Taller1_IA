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

    # TODO: Add your code here
    utils.raiseNotDefined()


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
