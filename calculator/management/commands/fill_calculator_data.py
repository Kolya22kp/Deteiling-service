from django.core.management.base import BaseCommand
from calculator.models import (
    VehicleType, BodyPart, FilmType, AdditionalOption, DiscountTier
)


class Command(BaseCommand):
    help = 'Заполняет базу данных калькулятора тестовыми данными из ТЗ Aureum Detail'

    def handle(self, *args, **options):
        # === 1. Типы автомобилей ===
        vehicle_types = {
            "Легковой автомобиль": 1.0,
            "Кроссовер / SUV": 1.2,
            "Внедорожник (крупный)": 1.4,
            "Минивэн / Микроавтобус": 1.6,
            "Коммерческий транспорт": 1.8,
            "Мотоцикл": 0.5,
        }
        vt_objects = {}
        for name, mult in vehicle_types.items():
            obj, created = VehicleType.objects.get_or_create(
                name=name,
                defaults={'base_multiplier': mult, 'is_active': True}
            )
            vt_objects[name] = obj
            self.stdout.write(f"{'✅ Создан' if created else '🔁 Уже есть'} тип: {name}")

        # === 2. Детали кузова (с ценами для ЛЕГКОВОГО) ===
        body_parts_data = [
            # Зона переда
            ("Капот (целиком)", 30000),
            ("Капот (частично, полоса 30-40 см)", 12000),
            ("Бампер передний (целиком)", 28000),
            ("Фара левая", 7000),
            ("Фара правая", 7000),
            ("Крыло переднее левое", 12000),
            ("Крыло переднее правое", 12000),

            # Зона боковин
            ("Дверь передняя левая", 15000),
            ("Дверь передняя правая", 15000),
            ("Дверь задняя левая", 15000),
            ("Дверь задняя правая", 15000),
            ("Порог левый", 8000),
            ("Порог правый", 8000),

            # Зона зада
            ("Багажник / Пятая дверь", 18000),
            ("Бампер задний (целиком)", 26000),
            ("Крыло заднее левое", 18000),
            ("Крыло заднее правое", 18000),

            # Зона верха
            ("Крыша (целиком)", 30000),
            ("Стойки крыши (комплект)", 10000),

            # Прочие элементы
            ("Зеркала боковые (пара)", 8000),
            ("Ручки дверные (комплект, 4 шт)", 6000),
            ("Зоны под ручками (комплект, 4 шт)", 4000),
        ]

        for name, price in body_parts_data:
            part, created = BodyPart.objects.get_or_create(
                name=name,
                defaults={'base_price': price, 'is_active': True}
            )
            # Связываем со всеми типами, кроме мотоцикла (если нужно — можно уточнить)
            part.vehicle_types.set(vt_objects.values())
            self.stdout.write(f"{'✅ Создана' if created else '🔁 Уже есть'} деталь: {name}")

        # === 3. Типы пленок ===
        film_types = [
            ("Глянцевая", 1.0),
            ("Матовая", 1.1),
            ("Карбон", 1.8),
            ("Хром / Color Shift", 2.2),
            ("Антиграффити (PPF)", 1.5),
        ]
        for name, mult in film_types:
            obj, created = FilmType.objects.get_or_create(
                name=name,
                defaults={'price_multiplier': mult, 'is_active': True}
            )
            self.stdout.write(f"{'✅ Создана' if created else '🔁 Уже есть'} пленка: {name}")

        # === 4. Доп. опции ===
        AdditionalOption.objects.get_or_create(
            name="Снятие/установка бампера",
            defaults={
                'price_fixed': 2000,
                'price_percent': None,
                'applies_to_body_part': True,
                'is_active': True
            }
        )
        AdditionalOption.objects.get_or_create(
            name="Антихром (оклейка хрома)",
            defaults={
                'price_fixed': 1500,
                'price_percent': None,
                'applies_to_body_part': True,
                'is_active': True
            }
        )
        AdditionalOption.objects.get_or_create(
            name="Подготовка кузова (полировка)",
            defaults={
                'price_fixed': None,
                'price_percent': 0.1,
                'applies_to_body_part': False,
                'is_active': True
            }
        )

        # === 5. Пороги скидок ===
        discount_tiers = [
            (0, 100000, 0),
            (100001, 250000, 5),
            (250001, 500000, 10),
            (500001, None, 15),
        ]
        for min_amt, max_amt, disc in discount_tiers:
            obj, created = DiscountTier.objects.get_or_create(
                min_amount=min_amt,
                max_amount=max_amt,
                defaults={'discount_percent': disc}
            )
            self.stdout.write(f"{'✅ Создан' if created else '🔁 Уже есть'} порог скидки: ≥{min_amt} → {disc}%")

        self.stdout.write(
            self.style.SUCCESS('✅ База данных калькулятора успешно заполнена!')
        )