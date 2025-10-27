from django.contrib import admin
from .models import (
    VehicleType, BodyPart, FilmType, AdditionalOption,
    DiscountTier, BookingRequest, SelectedBodyPart, SelectedOption, BodyZone
)

# Основные справочники
@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_multiplier', 'is_active')
    list_editable = ('is_active',)

@admin.register(BodyZone)
class BodyZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'base_price', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('zone', 'is_active')
    filter_horizontal = ('vehicle_types',)
    fields = ('name', 'zone', 'base_price', 'vehicle_types', 'is_active')

@admin.register(FilmType)
class FilmTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_multiplier', 'is_active')
    list_editable = ('is_active',)

@admin.register(AdditionalOption)
class AdditionalOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_fixed', 'price_percent', 'is_active')
    list_editable = ('is_active',)

@admin.register(DiscountTier)
class DiscountTierAdmin(admin.ModelAdmin):
    list_display = ('min_amount', 'max_amount', 'discount_percent')

# Заявки
class SelectedBodyPartInline(admin.TabularInline):
    model = SelectedBodyPart
    extra = 0
    readonly_fields = ('body_part', 'quantity')

class SelectedOptionInline(admin.TabularInline):
    model = SelectedOption
    extra = 0
    readonly_fields = ('option',)

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'total_price', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at', 'vehicle_type', 'film_type')
    list_editable = ('is_processed',)
    readonly_fields = (
        'name', 'phone', 'email', 'vehicle_type', 'film_type',
        'total_price', 'discount_applied', 'comment',
        'appointment_datetime', 'created_at'
    )
    ordering = ['-created_at']

    inlines = [SelectedBodyPartInline, SelectedOptionInline]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj:
            fields += ('selected_parts_summary', 'selected_options_summary')
        return fields

    def selected_parts_summary(self, obj):
        parts = obj.selected_parts.all()
        if not parts:
            return "—"
        return ", ".join([f"{p.body_part.name} ×{p.quantity}" for p in parts])
    selected_parts_summary.short_description = "Выбранные детали"

    def selected_options_summary(self, obj):
        options = obj.selected_options.all()
        if not options:
            return "—"
        return ", ".join([o.option.name for o in options])
    selected_options_summary.short_description = "Доп. опции"