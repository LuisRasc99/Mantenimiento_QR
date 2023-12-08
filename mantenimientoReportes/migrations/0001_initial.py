# Generated by Django 4.2.2 on 2023-12-08 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogoPartes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_partes', models.TextField(max_length=100)),
                ('numero_partes', models.TextField(max_length=20)),
                ('horas_vida', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_aproximado', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('foto_partes', models.ImageField(blank=True, null=True, upload_to='partes/')),
            ],
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maquina', models.TextField(max_length=100)),
                ('marca', models.TextField(max_length=100)),
                ('modelo', models.TextField(max_length=100)),
                ('horas_maquina', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nombre_maquina', models.TextField(blank=True, editable=False, max_length=100)),
                ('foto_maquina', models.ImageField(blank=True, null=True, upload_to='maquinas/')),
                ('qr', models.ImageField(blank=True, null=True, upload_to='qr/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('piezas_entrada', models.PositiveIntegerField(blank=True, null=True)),
                ('piezas_salida', models.PositiveIntegerField(blank=True, null=True)),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True)),
                ('fecha_salida', models.DateTimeField(auto_now_add=True)),
                ('costo_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_piezas', models.IntegerField(default=0)),
                ('new_horas_maquina', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('movimiento', models.BooleanField(default=True)),
                ('maquinas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimientoReportes.maquina')),
                ('partes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantenimientoReportes.catalogopartes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='catalogopartes',
            name='maquinas',
            field=models.ManyToManyField(related_name='partes', to='mantenimientoReportes.maquina'),
        ),
        migrations.AddField(
            model_name='catalogopartes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
