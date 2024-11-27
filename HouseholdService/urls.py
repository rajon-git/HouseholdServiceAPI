from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('service/', include('services.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    re_path(r'^(?:.*)?$', TemplateView.as_view(template_name="index.html")),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)