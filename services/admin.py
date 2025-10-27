from django.contrib import admin
from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('work_title', 'vehicle_make', 'vehicle_model', 'work_type')
    fields = (
        'work_title', 'work_description', 'vehicle_make', 'vehicle_model',
        'work_type', 'before_after',
        'work_image', 'alt_text',
        'work_image_two', 'alt_text_two'
    )