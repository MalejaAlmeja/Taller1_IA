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


def survivorHeuristic(state, problem):
    position, grid = state

    if grid.count() == 0:
        return 0

    survivor_coordinates = sorted(grid.asList())

    # Distancia al sobreviviente más cercano
    min_dist = min(
        abs(position[0] - x) + abs(position[1] - y)
        for (x, y) in survivor_coordinates
    )

    key = tuple(survivor_coordinates)

    if key not in problem.heuristicInfo:
        problem.heuristicInfo[key] = MST(survivor_coordinates)

    mst_cost = problem.heuristicInfo[key]

    return min_dist + mst_cost
        
        
    
    #Tengo otra idea:
    # 1. Hacer MST de los sobrevivientes restantes
    # 2. Tomar la distancia al sobreviviente más cercano
    # Pero no séeeeee
    # Usar lo de problem.heuristicInfo para guardar la distancia entre sobrevivientes 
    # y no tener que recalcularla cada vez maybe

    return min_survivor_distance
    
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
    
    
        
        
