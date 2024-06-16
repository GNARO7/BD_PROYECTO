from django.urls import path
from .views import *

urlpatterns = [
    path('indexAdministrador/', IndexAdminView.as_view(), name = 'indexAdmin'),
    
]