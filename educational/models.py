from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Слаг", unique=True, help_text="Используется в URL")
    short_description = models.TextField("Краткое описание", max_length=300)
    content = models.TextField("Полный текст статьи", help_text="Поддерживается HTML")
    reading_time_minutes = models.PositiveSmallIntegerField("Время чтения (минуты)")
    published_at = models.DateField("Дата публикации")
    image_url = models.URLField("URL изображения (превью)", max_length=500)
    hero_image_url = models.URLField("URL изображения (детальная)", max_length=500, blank=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})