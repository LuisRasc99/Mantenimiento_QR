# Generated by Django 4.2.2 on 2023-11-10 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoReportes', '0010_partes_inventarios_partes_maquinas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partes',
            name='inventarios',
        ),
        migrations.RemoveField(
            model_name='partes',
            name='maquinas',
        ),
        migrations.AddField(
            model_name='partes',
            name='inventarios',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='partes', to='mantenimientoReportes.inventario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partes',
            name='maquinas',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='partes', to='mantenimientoReportes.maquina'),
            preserve_default=False,
        ),
    ]
