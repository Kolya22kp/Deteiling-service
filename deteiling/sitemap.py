from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from educational.models import Article

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['index', 'calculator', 'about', 'privacy_policy', 'blog', 'services', 'gallery']

    def location(self, item):
        return reverse(item)

class ArticleSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return obj.get_absolute_url()
