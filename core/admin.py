from django.contrib import admin
from .models import ImageGallery, Privacypolicy, Settings, CallbackRequest
from django.utils import timezone


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image')
    fields = ('image', 'alt_text')

@admin.register(Privacypolicy)
class PrivacypolicyAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)
    fields = ('privacy_policy', 'updated_at')
    readonly_fields = ('updated_at',)

    def save_model(self, request, obj, form, change):
        obj.updated_at = timezone.now().date()
        super().save_model(request, obj, form, change)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fields = ('site_name', 'salon_address', 'salon_phone', 'salon_email', 'salon_tgk', 'ymap_widget')

    def has_add_permission(self, request):
        return not Settings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at', 'is_processed')
    list_editable = ('is_processed',)
    list_filter = ('is_processed', 'created_at')
    readonly_fields = ('name', 'phone', 'created_at')