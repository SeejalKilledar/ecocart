import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_model import forecast, PRODUCTS


def index(request):
    return render(request, 'inventory/index.html', {'products': list(enumerate(PRODUCTS))})


@csrf_exempt
def predict(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    product_index = int(data.get('product_index', 0))
    forecast_weeks = int(data.get('forecast_weeks', 8))
    result = forecast(product_index, forecast_weeks=forecast_weeks)
    return JsonResponse(result)
