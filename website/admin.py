# website/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Record  # Cambia esto si tu modelo tiene otro nombre
from django.contrib import admin

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        import website.signals  # Importar señales, este archivo lo crearemos

class RecordAdmin(admin.ModelAdmin):
    # Para que los Viewers no vean botones de agregar, editar ni eliminar
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Verificar permisos de agregar, actualizar y eliminar
        if not request.user.has_perm('website.add_record') and not request.user.has_perm('website.update_record') and not request.user.has_perm('website.delete_record'):
            qs = qs.none()  # No mostrar nada si no tiene ninguno de estos permisos
        return qs

admin.site.register(Record, RecordAdmin)
