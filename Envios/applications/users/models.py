from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class Usuario (AbstractBaseUser, PermissionsMixin):
    is_cliente = models.BooleanField(default = False)
    is_mensajero = models.BooleanField(default = False)
    username = models.CharField(max_length = 25, unique = True)
    nombres = models.CharField(max_length = 60, blank = True)
    apellidos = models.CharField(max_length = 60, blank = True)
    direccion = models.CharField(max_length = 60, blank=True, default = " ")
    email = models.EmailField(unique=False)
    telefono = models.CharField(max_length = 20, blank=True, default = " ")
    identificacion = models.CharField(max_length = 20)
    imagenPerfil = models.ImageField(upload_to='perfil_imagenes/', blank=False, null=True)

    USERNAME_FIELD = 'username'

    # campos 
    CIUDAD_CHOICES = (
        ('C','Santiago de Cali'),
        ('B','Bogota'),
        ('M','Medellin'),
        ('P','Pereira'),
    )

    ciudad = models.CharField(max_length = 100, choices = CIUDAD_CHOICES, blank = True)
    nombreSucursal = models.CharField(max_length=255, blank = True)
    telefonoSucursal = models.CharField(max_length = 20, blank = True)
    address_sucursal = models.CharField(max_length=255, blank = True)

    #campos mensajeros

    VEHICULO_CHICES = (
        ('M','Moto'),
        ('C','Carro'),
        ('F','Camion'),
    )

    vehiculo = models.CharField(max_length=1 , choices = VEHICULO_CHICES, blank = True)
    placaVehiculo = models.CharField(max_length = 6, blank = True)


    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomUserManager()

    def __str__(self):
        return str(self.id) + " - " + self.username
