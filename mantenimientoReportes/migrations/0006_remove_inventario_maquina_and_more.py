# Generated by Django 4.2.2 on 2023-11-29 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoReportes', '0005_inventario_inventario_stock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='maquina',
        ),
        migrations.RemoveField(
            model_name='inventariostock',
            name='maquina',
        ),
    ]
