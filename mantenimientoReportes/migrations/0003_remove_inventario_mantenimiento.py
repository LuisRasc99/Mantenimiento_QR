# Generated by Django 4.2.2 on 2023-11-26 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoReportes', '0002_alter_inventario_cantidad_piezas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='mantenimiento',
        ),
    ]
