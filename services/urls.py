from django.urls import path, include
from . import views

urlpatterns = [
    path('services/', views.services_page, name='services'),
    path('gallery/', views.gallery_page, name='gallery'),
]