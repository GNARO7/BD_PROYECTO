from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
#from .views import MensajeroCreateView, CustomLoginView, indexTemplateView, ClienteCreateView



urlpatterns = [
    path('create-mensajero/', MensajeroCreateView.as_view(), name='create_mensajero'),
    path('create-cliente/', ClienteCreateView.as_view(), name='create_cliente'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('mensajero/', PrincipalMensajeroView.as_view(), name='indexMensajero'),
    path('cliente/', PrincipalClienteView.as_view(), name='indexCliente'),
    path('logout/', logout_view, name='logout'),
    path('Actualizar-datos/<int:pk>/', UserUpdateView.as_view(), name='actualizarCliente'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('', home, name='home'),  # Esta será la URL de la página de inicio
    # Otras rutas...
]