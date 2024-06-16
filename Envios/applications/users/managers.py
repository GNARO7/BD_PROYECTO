from django.contrib.auth.models import BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, direccion, email, telefono, identificacion, 
                    ciudad, nombreSucursal, telefonoSucursal, address_sucursal, vehiculo, 
                    placaVehiculo, password=None, is_staff=False, is_superuser=False, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')
        if not direccion:
            raise ValueError('La dirección debe ser proporcionada')
        if not telefono:
            raise ValueError('El teléfono debe ser proporcionado')
        if not identificacion:
            raise ValueError('La identificación debe ser proporcionada')

        user = self.model(
            username=username,
            direccion=direccion,
            email=email,
            telefono=telefono,
            identificacion=identificacion,
            ciudad=ciudad,
            nombreSucursal=nombreSucursal,
            telefonoSucursal=telefonoSucursal,
            address_sucursal=address_sucursal,
            vehiculo=vehiculo,
            placaVehiculo=placaVehiculo,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, direccion="null", email="null", telefono="null", identificacion="null",
                         ciudad="null", nombreSucursal="null", telefonoSucursal="null", address_sucursal="null", vehiculo="C", 
                         placaVehiculo="null", password=None, **extra_fields):
        return self.create_user(username, direccion, email, telefono, identificacion,
                                ciudad, nombreSucursal, telefonoSucursal, address_sucursal, 
                                vehiculo, placaVehiculo, password, True, True, **extra_fields)

    

    def clientes(self):
        return self.filter(is_cliente = True)

    def mensajeros(self):
        return self.filter(is_mensajero = True)

    def por_ciudad(self, ciudad):
        return self.filter(ciudad=ciudad)
    

    
    


      