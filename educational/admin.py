from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'reading_time_minutes')
    list_filter = ('published_at',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')
    ordering = ('-published_at',)