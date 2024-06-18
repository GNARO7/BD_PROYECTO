from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


from .models import *

class ManajerServicios(models.Manager):

    def get_servicios_cliente(self, user):
        return self.filter(id_cliente=user)
    

    def get_servicios_disponibles_para_mensajero(self, mensajero):
        # Servicios que no tienen mensajero asignado y solicitan el vehículo del mensajero
        return self.filter(id_mensajero__isnull=True, vehiculoSolicitado=mensajero.vehiculo)
    
    def get_historial_servicios_mensajeros(self, mensajero):
        # Servicios que no tienen mensajero asignado y solicitan el vehículo del mensajero
        return self.filter(id_mensajero = mensajero, is_complete = True)
    

    def get_historial_servicios_cliente(self, cliente):
        # Servicios que no tienen mensajero asignado y solicitan el vehículo del mensajero
        return self.filter(id_cliente = cliente, is_complete = True)
    

    def get_servicio_actual(self, mensajero):
        
        # esta funcion me trae los servicios con el 
        return self.filter(id_mensajero = mensajero, is_complete = False).order_by('id').first()
    

    def tieneServicio(self, mensajero):
        if self.filter(id_mensajero = mensajero, is_complete = False).exists():
            return True
        else:
            return False
        
    def get_ciudades_con_mas_envios(self):
        return self.values('direccion_destino__ciudad').annotate(total=Count('id')).order_by('-total')[:10]
    
    def get_usuarios_con_mas_envios(self):
        return self.values('id_cliente__username').annotate(total_envios=Count('id')).order_by('-total_envios')[:10]
    

    def get_servicios_por_cliente_y_mes(self):
        return self.values('id_cliente__username') \
                   .annotate(mes=TruncMonth('fecha_creacion')) \
                   .values('id_cliente__username', 'mes') \
                   .annotate(total=Count('id')) \
                   .order_by('id_cliente__username', 'mes')

    def get_servicios_por_mensajero_y_mes(self, mes):
        return self.filter(fecha_creacion__month=mes) \
                   .values('id_mensajero__username') \
                   .annotate(total=Count('id')) \
                   .order_by('id_mensajero__username')

