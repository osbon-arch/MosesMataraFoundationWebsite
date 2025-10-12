from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('api/event-images/<int:event_id>/', views.event_images_api, name='event_images_api'),
    path('event-images/<int:event_id>/', views.event_images, name='event_images'),
]