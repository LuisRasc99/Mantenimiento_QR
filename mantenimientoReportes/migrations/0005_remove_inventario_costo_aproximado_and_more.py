# Generated by Django 4.2.2 on 2023-11-28 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoReportes', '0004_remove_inventario_fecha_entrada_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='costo_aproximado',
        ),
        migrations.AddField(
            model_name='catalogopartes',
            name='costo_aproximado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]