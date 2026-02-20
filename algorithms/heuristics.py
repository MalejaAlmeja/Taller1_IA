from typing import Any, Tuple
from algorithms import utils
from algorithms.problems import MultiSurvivorProblem


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.
    """
    return abs(state[0] - problem.goal[0]) + abs(state[1] - problem.goal[1])


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.
    """
    return ((state[0] - problem.goal[0]) ** 2 + (state[1] - problem.goal[1]) ** 2) ** 0.5


def realDist(pos1, pos2, problem):
    """Calcula la distancia real (con costos de terreno) entre dos posiciones usando UCS."""
    key = (pos1, pos2)
    reverse_key = (pos2, pos1)
    
    # Revisar caché en ambas direcciones
    if key in problem.heuristicInfo:
        return problem.heuristicInfo[key]
    if reverse_key in problem.heuristicInfo:
        return problem.heuristicInfo[reverse_key]
    
    # UCS desde pos1 hasta pos2
    pq = utils.PriorityQueue()
    pq.push(pos1, 0)
    visited = {}
    costs = {pos1: 0}

    while not pq.isEmpty():
        current = pq.pop()
        
        if current in visited:
            continue
        visited[current] = True
        
        if current == pos2:
            problem.heuristicInfo[key] = costs[pos2]
            return costs[pos2]
        
        x, y = current
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nextx, nexty = x + dx, y + dy
            next_pos = (nextx, nexty)
            
            if problem.walls[nextx][nexty]:
                continue
                
            step_cost = problem.startingMissionState.getTerrainCost(nextx, nexty)
            new_cost = costs[current] + step_cost
            
            if next_pos not in costs or costs[next_pos] > new_cost:
                costs[next_pos] = new_cost
                pq.update(next_pos, new_cost)
    
    # Si no hay camino (no debería pasar en mapas bien formados)
    problem.heuristicInfo[key] = float('inf')
    return float('inf')


def survivorHeuristic(state, problem):
    position, grid = state

    if grid.count() == 0:
        return 0

    survivor_coordinates = sorted(grid.asList())

    # Distancia real al sobreviviente más cercano
    min_dist = min(
        realDist(position, s, problem)
        for s in survivor_coordinates
    )

    # MST con distancias reales entre sobrevivientes
    key = tuple(survivor_coordinates)
    if key not in problem.heuristicInfo:
        problem.heuristicInfo[key] = realMST(survivor_coordinates, problem)

    return min_dist + problem.heuristicInfo[key]


def realMST(survivor_coordinates, problem):
    """MST de Prim usando distancias reales entre sobrevivientes."""
    if len(survivor_coordinates) <= 1:
        return 0

    visited = [survivor_coordinates[0]]
    no_visited = list(survivor_coordinates[1:])
    cost = 0

    while no_visited:
        min_edge = float('inf')
        next_node = None
        for v in visited:
            for u in no_visited:
                d = realDist(v, u, problem)
                if d < min_edge:
                    min_edge = d
                    next_node = u
        cost += min_edge
        visited.append(next_node)
        no_visited.remove(next_node)

    return cost
        
        
    
def MST(survivor_coordinates):
    #nos da el costo mínimo para visitar a los sobrevivientes restantes con distancia Manhattan
    #si hay 0-1 el costo sería 0
    if len(survivor_coordinates) <= 1:
        return 0
    visited = [survivor_coordinates[0]]
    no_visited = survivor_coordinates[1:]
    cost = 0 
    
    #visitar todos los sobrevivientes
    while len(no_visited) > 0:
        m_edge = float('inf')
        next = None
        for survivor in visited:
            for survivor2 in no_visited:
                #distancia entre sobreviviente y sobreviviente2 con Manhattan
                distancia = abs(survivor[0] - survivor2[0]) + abs(survivor[1] - survivor2[1])
                if distancia < m_edge:
                    m_edge = distancia
                    next = survivor2
        cost += m_edge
        visited.append(next)    
        no_visited.remove(next)
    return cost
    
    
        
        
