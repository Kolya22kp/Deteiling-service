from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_us_view, name='about'),
    path('privacy_policy/', views.privacy_policy_view, name='privacy_policy'),
    path('callback/', views.submit_callback, name='submit_callback'),
]