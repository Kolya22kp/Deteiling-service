import re

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Слаг", unique=True, help_text="Используется в URL. Не трогать")
    short_description = models.TextField("Краткое описание", max_length=300)
    content = models.TextField("Полный текст статьи", help_text="Поддерживается HTML")
    reading_time_minutes = models.PositiveSmallIntegerField("Время чтения (минуты)")
    published_at = models.DateField("Дата публикации")
    image_url = models.URLField("URL изображения (превью)", max_length=500)
    hero_image_url = models.URLField("URL изображения (детальная)", max_length=500, blank=True)

    def get_formatted_content(self):
        lines = self.content.split('\n')
        html_lines = []
        in_list = False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped == '[HR]':
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append('<hr>')
            elif stripped.startswith('[L]'):
                if not in_list:
                    if html_lines and html_lines[-1] != '<ul>':
                        html_lines.append('<ul>')
                    in_list = True
                item_text = self._process_inline_tags(stripped[3:].strip())
                html_lines.append(f'<li>{item_text}</li>')
            elif stripped.startswith('[T]'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                heading_text = self._process_inline_tags(stripped[3:].strip())
                html_lines.append(f'<h3>{heading_text}</h3>')
            elif stripped.startswith('[C]'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                quote_text = self._process_inline_tags(stripped[3:].strip())
                html_lines.append(f'<blockquote>{quote_text}</blockquote>')
            elif stripped.startswith('[P]'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                para_text = self._process_inline_tags(stripped[3:].strip())
                html_lines.append(f'<p>{para_text}</p>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                para_text = self._process_inline_tags(stripped)
                html_lines.append(f'<p>{para_text}</p>')

        if in_list:
            html_lines.append('</ul>')

        return mark_safe('\n'.join(html_lines))

    def _process_inline_tags(self, text):
        text = re.sub(r'\[B\](.*?)\[/B\]', r'<strong>\1</strong>', text)
        return text

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

