from .models import Settings

def site_settings(request):
    return {'site_settings': Settings.load()}