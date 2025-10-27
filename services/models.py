from django.db import models

class GalleryImage(models.Model):
    work_title = models.CharField(max_length=255)
    work_description = models.CharField(max_length=255)
    vehicle_make = models.CharField(max_length=255)
    vehicle_model = models.CharField(max_length=255)
    work_type = models.CharField(max_length=255, help_text="Только: exterior/interior, если не указывать - то будет показано как 'Индивидуальное решение'")
    before_after = models.BooleanField(default=False)
    work_image = models.ImageField(upload_to='gallery/')
    work_image_two = models.ImageField(upload_to='gallery/', default=None, help_text="Только если стоит галочка на before/after", blank=True)
    alt_text = models.CharField(max_length=200)
    alt_text_two = models.CharField(max_length=200, blank=True, help_text="Только если стоит галочка на before/after")

    class Meta:
        verbose_name = "Работа портфолио"
        verbose_name_plural = "Работы портфолио"

    def __str__(self):
        return self.work_title