from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('check-status/', views.check_status, name='check_status'),
]
