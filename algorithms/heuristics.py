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


def survivorHeuristic(state: Tuple[Tuple, Any], problem: MultiSurvivorProblem):
    """
    Your heuristic for the MultiSurvivorProblem.

    state: (position, survivors_grid)
    problem: MultiSurvivorProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider: distance to nearest survivor + MST of remaining survivors
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    problem.heuristicInfo
    # No quedan sobrevivientes
    if state[1].count() == 0:
        return 0
    
    min_survivor_distance = float('inf')
    #Tomar la distancia al sobreviviente más cercano
    grid = state[1]
    survivor_coordinates = grid.asList()
    for survivor in survivor_coordinates:
        #distancia al sobreviviente más cercano con Manhattan
        distance = abs(state[0][0] - survivor[0]) + abs(state[0][1] - survivor[1])
        min_survivor_distance = min(min_survivor_distance, distance)
    #la llave en heuristicInfo la calculamos como la tupla de survivor_coordinates en ese estado/ evita recalcular después 
    key = tuple(survivor_coordinates)
    #si no está en heuristicInfo se calcula y guarda y si ya está se saca de ahí 
    if key not in problem.heuristicInfo:
        problem.heuristicInfo[key] = MST(survivor_coordinates)
    mst = problem.heuristicInfo[key]
    
    return min_survivor_distance + mst
        
        
    

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
    
    
        
        
