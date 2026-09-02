import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .segmentation import run_segmentation


def index(request):
    return render(request, 'customer_segment/index.html')


@csrf_exempt
def analyze(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    biased = data.get('biased', True)
    result = run_segmentation(biased=biased)
    return JsonResponse(result)
