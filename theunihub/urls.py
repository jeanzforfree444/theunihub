from django.contrib import admin
from django.urls import path, include, reverse
from main import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

# Registration view that redirects to a profile registration page upon successful user registration
class HubRegistrationView(RegistrationView):
    
    def get_success_url(self, user):
    
        return reverse('main:register_profile')

handler404 = views.Custom404View.as_view()

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('main/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('accounts/register/', HubRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)