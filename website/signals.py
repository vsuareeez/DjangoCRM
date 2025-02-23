# website/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Record  # Ajusta esto si el nombre de tu modelo es diferente

"""@receiver(post_migrate)
def create_roles(sender, **kwargs):
    # Crear grupos de roles: Admin y Viewer
    roles = ['Admin', 'Viewer']
    for role in roles:
        group, created = Group.objects.get_or_create(name=role)

        # Asignar permisos a los grupos
        content_type = ContentType.objects.get_for_model(Record)  # Asegúrate de usar el modelo correcto
        if role == 'Admin':
            permissions = Permission.objects.filter(content_type=content_type)
        else:  # 'Viewer'
            permissions = Permission.objects.filter(content_type=content_type, codename__startswith='view')

        group.permissions.set(permissions)
        group.save()"""
