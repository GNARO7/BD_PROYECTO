# Generated by Django 5.0.2 on 2024-06-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0006_servicio_imagenestado_alter_direccion_ciudad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='imagenEstado',
            field=models.ImageField(blank=True, null=True, upload_to='estado_imagenes/'),
        ),
    ]
