from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resultados', '0002_rename_meta_mantenimiento'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Periodo',
            new_name='Trimestre',
        ),
        migrations.RenameField(
            model_name='metamantenimiento',
            old_name='periodo',
            new_name='trimestre',
        ),
    ]
