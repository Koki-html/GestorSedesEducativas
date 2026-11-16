from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


CUSTOM_APPS = ('organizacion', 'actividades', 'agenda', 'resultados')


class Command(BaseCommand):
    help = 'Configura los grupos Consulta (solo lectura) y Gestion (CRUD).'

    def handle(self, *args, **options):
        content_types = ContentType.objects.filter(app_label__in=CUSTOM_APPS)
        permissions = Permission.objects.filter(content_type__in=content_types)

        consulta, _ = Group.objects.get_or_create(name='Consulta')
        consulta.permissions.set(permissions.filter(codename__startswith='view_'))

        gestion, _ = Group.objects.get_or_create(name='Gestion')
        gestion.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                'Permisos configurados: Consulta solo puede ver y Gestion puede administrar.'
            )
        )
