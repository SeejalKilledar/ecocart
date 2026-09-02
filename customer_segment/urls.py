from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='customer_segment'),
    path('analyze/', views.analyze, name='analyze'),
]
