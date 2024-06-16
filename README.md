# Proyecto Bases de Datos

## Pasos para ejecutar el proyecto:

1. *Instalar Docker*:
   - Asegúrate de tener Docker instalado y de haber iniciado sesión.

2. *Navegar al directorio del proyecto*:
   - Abre una terminal y navega al directorio que contiene el archivo docker-compose.yml.

3. *Construir y levantar los contenedores*:
   - Ejecuta el siguiente comando:
     bash
     docker-compose up --build
     

4. *Módulo Admin*:
   - Para el módulo de administrador, se inicia sesión desde el mismo login de los usuarios.

### Creación de un Superusuario

1. *Abrir la terminal del contenedor del proyecto*:
   - Ejecuta el siguiente comando para crear un superusuario:
     bash
     python manage.py createsuperuser
     

2. *Agregar una imagen de perfil al superusuario*:
   - Antes de hacer login con el admin, es necesario agregar una imagen de perfil.
   - Ingresa a la siguiente URL (el contenedor debe estar activo):
     
     http://localhost:8000/admin
     
   - Haz login y en la sección de usuarios, selecciona la cuenta creada y agrégale una imagen y un correo electrónico.
