from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    
    path('gallery/', views.gallery, name='gallery'),
    path('api/event-images/<int:event_id>/', views.event_images_api, name='event_images_api'),
    path('event-images/<int:event_id>/', views.event_images, name='event_images'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path("contact/", views.contact, name="contact"),

]