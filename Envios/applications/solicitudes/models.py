import time
from typing import Iterable
from django.db import models
from applications.users.models import Usuario
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from .managers import ManajerServicios

# Create your models here.

class Direccion(models.Model):
    direccion = models.CharField(max_length=300)
    CIUDAD_CHOICES = (
        ('C','Santiago de Cali'),
        ('B','Bogota'),
        ('M','Medellin'),
        ('P','Pereira'),
    )
    ciudad = models.CharField(max_length=100, choices = CIUDAD_CHOICES)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    #manager
    

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    

    def __str__(self):
        return f'{self.direccion}, {self.ciudad}, {self.departamento}, {self.pais}, {self.codigo_postal}'

    def save(self, *args, **kwargs):
        if not self.latitud or not self.longitud:
            geolocator = Nominatim(user_agent="Express", timeout = 5)
            full_address = f'{self.direccion} {self.codigo_postal}, {self.ciudad}, {self.departamento}, {self.pais}'
            try:
                location = geolocator.geocode(full_address)
                if location:
                    self.latitud = location.latitude
                    self.longitud = location.longitude
                else:
                    print("No se encontro la direccion.")
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"Error al geocodificar la dirección: {e}")
            time.sleep(1)

        super(Direccion, self).save(*args, **kwargs)





class Servicio(models.Model):
    id_cliente = models.ForeignKey(Usuario, 
                                   on_delete=models.CASCADE, 
                                   related_name='servicios_cliente', 
                                   blank=False, 
                                   null=False)
    id_mensajero = models.ForeignKey(Usuario, 
                                     on_delete=models.CASCADE, 
                                     related_name='servicios_mensajero', 
                                     blank=True, 
                                     null=True)
    
    VEHICULO_CHICES = (
        ('M','Moto'),
        ('C','Carro'),
        ('F','Camion'),
    )

    vehiculoSolicitado = models.CharField(max_length=1 , choices = VEHICULO_CHICES, blank = True)
    direccion_recojer = models.ForeignKey(Direccion, on_delete = models.CASCADE, related_name = 'direccion1', blank = False, null = False)
    direccion_destino = models.ForeignKey(Direccion, on_delete = models.CASCADE, related_name = 'direccion2', blank = False, null = False)
    SERVICIO_ESTADOS = (
        ('S', 'Solicitado.'),
        ('A', 'Agendado, un mensajero tomo tu pedido.'),
        ('C', 'Tu envío está en camino.'),
        ('D', 'Tu envío ha llegado a su destino.'),
        ('E', 'Tu envío ha sido entregado.'),
    )


    imagenEstado = models.ImageField(upload_to='estado_imagenes/', blank=True, null=True)


    estados = models.CharField(max_length=1, choices=SERVICIO_ESTADOS, blank=True)
    descripcion = models.CharField(max_length=300, null=False, blank=False)
    is_complete = models.BooleanField(blank = True, null = True, default = False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    objects = models.Manager()  # Manager por defecto
    servicios_cliente = ManajerServicios()  # Manager personalizado


    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):  
        return f'Servicio {self.id} - {self.descripcion}'
