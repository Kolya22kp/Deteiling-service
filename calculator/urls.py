from django.urls import path
from . import views

urlpatterns = [
    path('calculator/', views.calculator_view, name='calculator'),
    path('calculator/api/submit-booking/', views.submit_booking, name='submit_booking'),
]
