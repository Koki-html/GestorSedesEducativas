from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resultados', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Meta',
            new_name='MetaMantenimiento',
        ),
    ]
