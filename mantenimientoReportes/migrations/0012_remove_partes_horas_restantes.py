# Generated by Django 4.2.2 on 2023-11-10 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoReportes', '0011_remove_partes_inventarios_remove_partes_maquinas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partes',
            name='horas_restantes',
        ),
    ]
