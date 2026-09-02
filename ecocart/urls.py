from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('route/', include('route_optimizer.urls')),
    path('inventory/', include('inventory.urls')),
    path('segment/', include('customer_segment.urls')),
]
