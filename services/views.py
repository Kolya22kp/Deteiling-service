import json
from django.shortcuts import render
from django.http import HttpResponse

from services.models import GalleryImage


def services_page(request):
    return render(request, 'pages/services.html')

def gallery_page(request):
    works = GalleryImage.objects.filter(
        vehicle_make__isnull=False,
        vehicle_model__isnull=False
    ).values('vehicle_make', 'vehicle_model').distinct()
    car_data = {}
    for work in works:
        make = work['vehicle_make'].strip().lower()
        model = work['vehicle_model'].strip()
        if make and model:
            if make not in car_data:
                car_data[make] = set()
            car_data[make].add(model)

    car_data = {make: sorted(list(models)) for make, models in car_data.items()}

    gallery_images = GalleryImage.objects.all()

    makes = sorted(set(img.vehicle_make for img in gallery_images if img.vehicle_make))
    work_types = sorted(set(img.work_type for img in gallery_images if img.work_type))


    models_by_make = {}
    for img in gallery_images:
        if img.vehicle_make and img.vehicle_model:
            make_key = img.vehicle_make.strip().lower()
            model = img.vehicle_model.strip()
            if make_key not in models_by_make:
                models_by_make[make_key] = set()
            models_by_make[make_key].add(model)

    models_by_make = {
        make: sorted(list(models))
        for make, models in models_by_make.items()
    }


    context = {
        "works": GalleryImage.objects.all(),
        'car_data_json': json.dumps(car_data, ensure_ascii=False),
        'gallery_images': gallery_images,
        'makes_json': json.dumps(makes, ensure_ascii=False),
        'models_by_make_json': json.dumps(models_by_make, ensure_ascii=False),
        'work_types_json': json.dumps(work_types, ensure_ascii=False),
    }
    return render(request, 'pages/gallery.html', context=context)