from django.conf import settings

def translator_api_key(request):
    
    return {"TRANSLATOR_API_KEY": getattr(settings, "TRANSLATOR_API_KEY", "")}