"""
EcoCart Route Optimization Algorithms
Implements DFS, BFS, A*, and IDA* for delivery route planning.
"""
import math
import time
from collections import deque
import heapq

# ── Sample EcoCart delivery network ──────────────────────────────────────────
GRAPH = {
    'Warehouse':  {'Market_A': 4, 'Suburb_B': 2, 'Rural_C': 7},
    'Market_A':   {'Warehouse': 4, 'Hub_D': 5, 'Market_E': 3},
    'Suburb_B':   {'Warehouse': 2, 'Market_A': 1, 'Rural_F': 4},
    'Rural_C':    {'Warehouse': 7, 'Hub_D': 3, 'Rural_G': 2},
    'Hub_D':      {'Market_A': 5, 'Rural_C': 3, 'Depot_H': 4},
    'Market_E':   {'Market_A': 3, 'Depot_H': 6},
    'Rural_F':    {'Suburb_B': 4, 'Rural_G': 3, 'Depot_H': 5},
    'Rural_G':    {'Rural_C': 2, 'Rural_F': 3, 'Depot_H': 2},
    'Depot_H':    {'Hub_D': 4, 'Market_E': 6, 'Rural_F': 5, 'Rural_G': 2},
}

# Coordinates (x, y) for A* Euclidean heuristic
COORDINATES = {
    'Warehouse': (0, 0),
    'Market_A':  (2, 3),
    'Suburb_B':  (1, -1),
    'Rural_C':   (-2, 3),
    'Hub_D':     (0, 5),
    'Market_E':  (4, 4),
    'Rural_F':   (2, -2),
    'Rural_G':   (-1, 2),
    'Depot_H':   (2, 1),
}

NODES = list(GRAPH.keys())


def heuristic(a, b):
    ax, ay = COORDINATES[a]
    bx, by = COORDINATES[b]
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


# ── DFS ───────────────────────────────────────────────────────────────────────
def dfs(start, goal):
    start_time = time.perf_counter()
    visited_order = []
    stack = [(start, [start], 0)]
    visited = set()

    while stack:
        node, path, cost = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        visited_order.append(node)

        if node == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                'algorithm': 'DFS',
                'path': path,
                'cost': cost,
                'nodes_visited': visited_order,
                'nodes_count': len(visited_order),
                'time_ms': round(elapsed, 4),
                'found': True,
            }

        for neighbour, weight in sorted(GRAPH[node].items(), reverse=True):
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour], cost + weight))

    return {'algorithm': 'DFS', 'found': False, 'nodes_visited': visited_order}


# ── BFS ───────────────────────────────────────────────────────────────────────
def bfs(start, goal):
    start_time = time.perf_counter()
    visited_order = []
    queue = deque([(start, [start], 0)])
    visited = {start}

    while queue:
        node, path, cost = queue.popleft()
        visited_order.append(node)

        if node == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                'algorithm': 'BFS',
                'path': path,
                'cost': cost,
                'nodes_visited': visited_order,
                'nodes_count': len(visited_order),
                'time_ms': round(elapsed, 4),
                'found': True,
            }

        for neighbour, weight in sorted(GRAPH[node].items()):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour], cost + weight))

    return {'algorithm': 'BFS', 'found': False, 'nodes_visited': visited_order}


# ── A* ────────────────────────────────────────────────────────────────────────
def astar(start, goal):
    start_time = time.perf_counter()
    visited_order = []
    open_set = [(heuristic(start, goal), 0, start, [start])]
    g_scores = {start: 0}

    while open_set:
        f, g, node, path = heapq.heappop(open_set)
        if node in [n for n in visited_order]:
            continue
        visited_order.append(node)

        if node == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                'algorithm': 'A*',
                'path': path,
                'cost': g,
                'nodes_visited': visited_order,
                'nodes_count': len(visited_order),
                'time_ms': round(elapsed, 4),
                'found': True,
            }

        for neighbour, weight in GRAPH[node].items():
            tentative_g = g + weight
            if tentative_g < g_scores.get(neighbour, float('inf')):
                g_scores[neighbour] = tentative_g
                f_score = tentative_g + heuristic(neighbour, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbour, path + [neighbour]))

    return {'algorithm': 'A*', 'found': False, 'nodes_visited': visited_order}


# ── IDA* ──────────────────────────────────────────────────────────────────────
def idastar(start, goal):
    start_time = time.perf_counter()
    visited_order = []

    def search(path, g, bound):
        node = path[-1]
        f = g + heuristic(node, goal)
        if f > bound:
            return f, None
        if node == goal:
            return -1, list(path)
        minimum = float('inf')
        for neighbour, weight in sorted(GRAPH[node].items()):
            if neighbour not in path:
                visited_order.append(neighbour)
                path.append(neighbour)
                t, result = search(path, g + weight, bound)
                if t == -1:
                    return -1, result
                if t < minimum:
                    minimum = t
                path.pop()
        return minimum, None

    bound = heuristic(start, goal)
    path = [start]
    visited_order.append(start)

    while True:
        t, result = search(path, 0, bound)
        if t == -1 and result:
            # Calculate cost
            cost = sum(GRAPH[result[i]][result[i + 1]] for i in range(len(result) - 1))
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                'algorithm': 'IDA*',
                'path': result,
                'cost': cost,
                'nodes_visited': visited_order,
                'nodes_count': len(visited_order),
                'time_ms': round(elapsed, 4),
                'found': True,
            }
        if t == float('inf'):
            return {'algorithm': 'IDA*', 'found': False, 'nodes_visited': visited_order}
        bound = t


def run_all(start, goal):
    """Run all four algorithms and return comparative results."""
    return [
        dfs(start, goal),
        bfs(start, goal),
        astar(start, goal),
        idastar(start, goal),
    ]
