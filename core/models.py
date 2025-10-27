from django.db import models


class ImageGallery(models.Model):
    image = models.ImageField(upload_to="index_gallery/", blank=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Надпись при наведении на текст или при незагрузке изображения")

    class Meta:
        verbose_name = "Работа на главной странице"
        verbose_name_plural = "Работы на главной странице"

    def __str__(self):
        return 'Работы на главной странице'

class Privacypolicy(models.Model):
    privacy_policy = models.TextField()
    updated_at = models.DateField(auto_now=True, help_text="Не трогать")

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политики конфиденциальности"

    def __str__(self):
        return 'Политика конфиденциальности'

class Settings(models.Model):
    site_name = models.CharField("Название сайта", max_length=200)
    salon_address = models.TextField("Адрес салона")
    salon_phone = models.CharField("Телефон салона", max_length=20)
    salon_email = models.EmailField("Email салона")
    salon_tgk = models.CharField("Ссылка на Telegram канал", blank=True)
    ymap_widget = models.CharField("Ссылка на виджет YMaps", blank=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Основные настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class CallbackRequest(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_processed = models.BooleanField("Обработана", default=False)

    class Meta:
        verbose_name = "Заявка на обратный звонок"
        verbose_name_plural = "Заявки на обратный звонок"
        ordering = ['-created_at']

    def __str__(self):
        return f"Звонок {self.name} ({self.phone})"