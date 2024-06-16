# Generated by Django 5.0.2 on 2024-06-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0005_servicio_fecha_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='imagenEstado',
            field=models.ImageField(null=True, upload_to='estado_imagenes/'),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='ciudad',
            field=models.CharField(choices=[('C', 'Santiago de Cali'), ('B', 'Bogota'), ('M', 'Medellin'), ('P', 'Pereira')], max_length=100),
        ),
    ]
