# Generated by Django 4.2.2 on 2023-11-26 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoReportes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='cantidad_piezas',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='piezas_entrada',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mantenimientopartes',
            name='piezas_salida',
            field=models.IntegerField(default=0),
        ),
    ]