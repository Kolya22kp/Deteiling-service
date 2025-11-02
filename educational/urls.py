from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.article_list, name='blog'),
    path('blog/<slug:slug>/', views.article_detail, name='article_detail'),
]