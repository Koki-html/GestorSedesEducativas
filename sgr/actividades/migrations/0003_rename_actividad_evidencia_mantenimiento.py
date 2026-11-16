from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_remove_actividad_fecha_fin_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Actividad',
            new_name='ActividadMantenimiento',
        ),
        migrations.RenameModel(
            old_name='Evidencia',
            new_name='EvidenciaMantenimiento',
        ),
    ]
