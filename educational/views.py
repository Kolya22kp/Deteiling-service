from django.shortcuts import render
from .models import Article

def article_page(request):
    articles = Article.objects.all()
    return render(request, 'pages/blog.html', {'articles': articles})