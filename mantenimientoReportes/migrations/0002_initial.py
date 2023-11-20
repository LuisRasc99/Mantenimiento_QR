# Generated by Django 4.2.2 on 2023-11-20 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mantenimientoReportes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mantenimientopartes',
            name='maquina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mantenimiento', to='mantenimientoReportes.maquina'),
        ),
        migrations.AddField(
            model_name='mantenimientopartes',
            name='partes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mantenimiento', to='mantenimientoReportes.catalogopartes'),
        ),
        migrations.AddField(
            model_name='mantenimientopartes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventario',
            name='mantenimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario', to='mantenimientoReportes.mantenimientopartes'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='maquina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario', to='mantenimientoReportes.maquina'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='partes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario', to='mantenimientoReportes.catalogopartes'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='catalogopartes',
            name='maquina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partes', to='mantenimientoReportes.maquina'),
        ),
        migrations.AddField(
            model_name='catalogopartes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
