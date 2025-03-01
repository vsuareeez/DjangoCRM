from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Primero defines 'urlpatterns' como una lista
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('calendar/', include('calendar_app.urls')),
]

# Luego puedes agregar las rutas para archivos estáticos (media files)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
