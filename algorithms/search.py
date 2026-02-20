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
    Search the shallowest nodes in the search tree first.
    """

    #Version inicial BFS

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
    Search the node of least total cost first.
    """
    #Version inicial UCS

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
    Search the node that has the lowest combined cost and heuristic first.
    """
    #Version inicial A*
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
