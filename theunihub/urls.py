from django.contrib import admin
from django.urls import path, include, reverse
from main import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

class HubRegistrationView(RegistrationView):
    
    def get_success_url(self, user):
    
        return reverse('main:register_profile')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('main/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('accounts/register/', HubRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)