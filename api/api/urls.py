from django.urls import path, re_path
from . import views

urlpatterns = [
    path('databatch/', views.api_databatch),
    path('<collection>/', views.api),
]
