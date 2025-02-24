# website/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Record, Note # Cambia esto si tu modelo tiene otro nombre
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        import website.signals  # Importar señales, este archivo lo crearemos

class RecordAdmin(SimpleHistoryAdmin):
    # Para que los Viewers no vean botones de agregar, editar ni eliminar
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Verificar permisos de agregar, actualizar y eliminar
        if not request.user.has_perm('website.add_record') and not request.user.has_perm('website.update_record') and not request.user.has_perm('website.delete_record'):
            qs = qs.none()  # No mostrar nada si no tiene ninguno de estos permisos
        return qs

class NoteAdmin(admin.ModelAdmin):
    list_display = ('client', 'author', 'created_at')
    search_fields = ('client__name', 'author__username', 'content')

admin.site.register(Note, NoteAdmin)
admin.site.register(Record, RecordAdmin)
