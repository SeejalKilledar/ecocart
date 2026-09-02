import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .algorithms import GRAPH, COORDINATES, NODES, run_all, dfs, bfs, astar, idastar


def index(request):
    graph_data = {
        'nodes': [{'id': n, 'x': COORDINATES[n][0], 'y': COORDINATES[n][1]} for n in NODES],
        'edges': [],
    }
    seen = set()
    for node, neighbours in GRAPH.items():
        for nb, weight in neighbours.items():
            key = tuple(sorted([node, nb]))
            if key not in seen:
                seen.add(key)
                graph_data['edges'].append({'from': node, 'to': nb, 'weight': weight})

    return render(request, 'route_optimizer/index.html', {
        'nodes': NODES,
        'graph_json': json.dumps(graph_data),
    })


@csrf_exempt
def optimize(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)
    start = data.get('start', 'Warehouse')
    goal = data.get('goal', 'Depot_H')
    algorithm = data.get('algorithm', 'all')

    if start not in GRAPH or goal not in GRAPH:
        return JsonResponse({'error': 'Invalid node'}, status=400)

    algo_map = {'dfs': dfs, 'bfs': bfs, 'astar': astar, 'idastar': idastar}

    if algorithm == 'all':
        results = run_all(start, goal)
    elif algorithm in algo_map:
        results = [algo_map[algorithm](start, goal)]
    else:
        return JsonResponse({'error': 'Unknown algorithm'}, status=400)

    return JsonResponse({'results': results})
