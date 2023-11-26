# Generated by Django 4.2.2 on 2023-09-19 23:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoSLOGIN', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operadores',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('calle', models.CharField(max_length=100)),
                ('numero_calle', models.CharField(max_length=100)),
                ('colonia', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('telefono', models.CharField(max_length=15)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
