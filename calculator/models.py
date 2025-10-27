from django.db import models
from django.core.validators import MinValueValidator


class VehicleType(models.Model):
    name = models.CharField("Название типа", max_length=100, unique=True)
    base_multiplier = models.FloatField(
        "Базовый коэффициент сложности",
        default=1.0,
    )
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Тип автомобиля"
        verbose_name_plural = "Типы автомобилей"
        ordering = ['id']

    def __str__(self):
        return self.name

class BodyZone(models.Model):
    name = models.CharField("Название зоны", max_length=100, unique=True)
    order = models.PositiveSmallIntegerField("Порядок отображения", default=0)

    class Meta:
        verbose_name = "Зона кузова"
        verbose_name_plural = "Зоны кузова"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BodyPart(models.Model):
    name = models.CharField("Название детали", max_length=100, unique=True)
    base_price = models.DecimalField(
        "Базовая цена",
        max_digits=10,
        decimal_places=2,
    )
    zone = models.ForeignKey(
        BodyZone,
        on_delete=models.PROTECT,
        verbose_name="Зона кузова",
        null=True,
        blank=True,
    )
    vehicle_types = models.ManyToManyField(
        VehicleType,
        verbose_name="Поддерживаемые типы авто",
        blank=True,
    )
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Деталь кузова"
        verbose_name_plural = "Детали кузова"
        ordering = ['name']

    def __str__(self):
        return self.name


class FilmType(models.Model):
    name = models.CharField("Название пленки", max_length=100, unique=True)
    price_multiplier = models.FloatField(
        "Множитель цены",
        default=1.0,
    )
    description = models.TextField("Описание", blank=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Тип пленки"
        verbose_name_plural = "Типы пленок"

    def __str__(self):
        return f"{self.name} (×{self.price_multiplier})"


class AdditionalOption(models.Model):
    name = models.CharField("Название опции", max_length=150)
    price_fixed = models.DecimalField(
        "Фиксированная цена",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    price_percent = models.FloatField(
        "Процент от стоимости детали",
        blank=True,
        null=True,
        help_text="Например: 10% = 0.1"
    )
    applies_to_body_part = models.BooleanField(
        "Применяется к выбранным деталям",
        default=True,
    )
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Дополнительная опция"
        verbose_name_plural = "Дополнительные опции"

    def __str__(self):
        if self.price_fixed is not None:
            return f"{self.name} (+{self.price_fixed} ₽)"
        elif self.price_percent is not None:
            return f"{self.name} (+{int(self.price_percent * 100)}%)"
        return self.name


class DiscountTier(models.Model):
    min_amount = models.DecimalField(
        "Минимальная сумма",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    max_amount = models.DecimalField(
        "Максимальная сумма (оставьте пустым для 'и выше')",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    discount_percent = models.FloatField(
        "Скидка (%)",
        validators=[MinValueValidator(0), MinValueValidator(100)]
    )

    class Meta:
        verbose_name = "Порог скидки"
        verbose_name_plural = "Пороги скидок"
        ordering = ['min_amount']

    def __str__(self):
        if self.max_amount is None:
            return f"От {self.min_amount} ₽ → {self.discount_percent}%"
        return f"{self.min_amount}–{self.max_amount} ₽ → {self.discount_percent}%"


class BookingRequest(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email", blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, verbose_name="Тип авто")
    film_type = models.ForeignKey(FilmType, on_delete=models.PROTECT, verbose_name="Тип пленки")
    total_price = models.DecimalField("Итоговая цена", max_digits=12, decimal_places=2)
    discount_applied = models.FloatField("Скидка (%)", default=0)
    comment = models.TextField("Комментарий", blank=True)
    appointment_datetime = models.DateTimeField("Желаемое время записи", null=True, blank=True)
    is_processed = models.BooleanField("Обработана", default=False)

    class Meta:
        verbose_name = "Заявка на оклейку"
        verbose_name_plural = "Заявки на оклейку"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.name} ({self.created_at.strftime('%d.%m.%Y')})"


class SelectedBodyPart(models.Model):
    booking = models.ForeignKey(BookingRequest, related_name='selected_parts', on_delete=models.CASCADE)
    body_part = models.ForeignKey(BodyPart, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Выбранная деталь"
        verbose_name_plural = "Выбранные детали"

    def __str__(self):
        return f"{self.body_part.name} ×{self.quantity}"


class SelectedOption(models.Model):
    booking = models.ForeignKey(BookingRequest, related_name='selected_options', on_delete=models.CASCADE)
    option = models.ForeignKey(AdditionalOption, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Выбранная опция"
        verbose_name_plural = "Выбранные опции"