# Generated by Django 4.2.2 on 2023-10-04 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mantenimientoSLOGIN', '0004_tecnicos_delete_operadores'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosTecnicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('calle', models.CharField(max_length=100)),
                ('numero_calle', models.CharField(max_length=100)),
                ('colonia', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('telefono', models.CharField(max_length=15)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('foto_tecnico', models.ImageField(blank=True, null=True, upload_to='tecnicos/')),
                ('rol', models.CharField(choices=[('administrador', 'Administrador'), ('tecnico', 'Técnico')], default='tecnico', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='datosusuario',
            name='foto_user',
            field=models.ImageField(blank=True, null=True, upload_to='administradores/'),
        ),
        migrations.AddField(
            model_name='datosusuario',
            name='rol',
            field=models.CharField(choices=[('administrador', 'Administrador'), ('tecnico', 'Técnico')], default='administrador', max_length=20),
        ),
        migrations.DeleteModel(
            name='Tecnicos',
        ),
    ]