from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='route_optimizer'),
    path('optimize/', views.optimize, name='optimize'),
]
