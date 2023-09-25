# Generated by Django 4.2.2 on 2023-09-25 04:13

from django.db import migrations, models
import mantenimientoSLOGIN.models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoSLOGIN', '0004_tecnicos_delete_operadores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tecnicos',
            name='foto',
        ),
        migrations.AddField(
            model_name='tecnicos',
            name='foto_tecnico',
            field=models.ImageField(blank=True, null=True, upload_to=mantenimientoSLOGIN.models.imagen_tecnico_path),
        ),
    ]
