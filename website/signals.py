# website/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Record


@receiver(post_migrate)
def create_roles(sender, **kwargs):
    # Solo ejecutar cuando migra esta app, para no correr en cada post_migrate
    if getattr(sender, 'name', None) != 'website':
        return

    # Crear grupos de roles: Admin y Viewer
    content_type = ContentType.objects.get_for_model(Record)
    roles = ['Admin', 'Viewer']
    for role in roles:
        group, created = Group.objects.get_or_create(name=role)

        # Asignar permisos a los grupos
        if role == 'Admin':
            permissions = Permission.objects.filter(content_type=content_type)
        else:  # 'Viewer'
            permissions = Permission.objects.filter(content_type=content_type, codename__startswith='view')

        group.permissions.set(permissions)
