# Generated by Django 4.2.2 on 2023-11-21 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientoSLOGIN', '0006_rename_usuario_datosusuario_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosusuario',
            name='cp',
            field=models.IntegerField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='datosusuario',
            name='numero_calle',
            field=models.IntegerField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='datosusuario',
            name='telefono',
            field=models.IntegerField(default='', null=True),
        ),
    ]