from django.views.generic import View, TemplateView, ListView
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Direccion, Servicio
from .forms import DireccionForm, ServicioForm, ServicioEstadoForm, ServicioFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import make_aware
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


class CrearServicioView(View, LoginRequiredMixin):

    #esta es la funcion get, basicamente, desde aca se mandan los formularios 
    def get(self, request, *args, **kwargs):
        # se usa un form set por que son dos formularios de tipo direccion al mismo tiempo
        direccion_formset = modelformset_factory(Direccion, form=DireccionForm, extra=2)
        formset = direccion_formset(queryset=Direccion.objects.none())
        servicio_form = ServicioForm()
        return render(request, 'servicios/crearServicio.html', {'formset': formset, 'servicio_form': servicio_form})

    
    def post(self, request, *args, **kwargs):
        direccion_formset = modelformset_factory(Direccion, form=DireccionForm, extra=2)
        formset = direccion_formset(request.POST)
        servicio_form = ServicioForm(request.POST)

        if formset.is_valid() and servicio_form.is_valid():
            # cuardar las direcciones
            direcciones = formset.save()
            # crear y guardar el servicio asignando las direcciones
            servicio = servicio_form.save(commit=False)
            servicio.direccion_recojer = direcciones[0]
            servicio.direccion_destino = direcciones[1]
            servicio.estados = 'S'
            servicio.id_cliente = request.user 
            servicio.id_mensajero = None 
            servicio.is_complete = False
            servicio.save()
            return redirect('servicio_list')

        return render(request, 'servicios/crearServicio.html', {'formset': formset, 'servicio_form': servicio_form})


class ClienteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_cliente

class MensajeroRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_mensajero    


class VerServiciosCliente(TemplateView):
    template_name = "servicios/serviciosEstado.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios = Servicio.servicios_cliente.get_servicios_cliente(self.request.user)
        print(servicios)
        context['servicios'] = servicios
        return context
    

class ServiciosDisponiblesParaMensajeroView(MensajeroRequiredMixin, ListView):
    template_name = "servicios/serviciosMensajero.html"
    context_object_name = 'servicios'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_mensajero and not Servicio.servicios_cliente.tieneServicio(usuario):
            return Servicio.servicios_cliente.get_servicios_disponibles_para_mensajero(usuario)
        return Servicio.objects.none()
    

class AceptarServicioView(MensajeroRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        servicio_id = kwargs.get('servicio_id')
        servicio = get_object_or_404(Servicio, id=servicio_id)
        
        if servicio.id_mensajero is None:
            servicio.id_mensajero = request.user
            servicio.estados = 'A'  # Cambiar el estado del servicio si es necesario
            servicio.save()
            return redirect('indexMensajero')
        else:
            return redirect('ver_servicios_disponibles')  # O algún mensaje de error



class GestionarServicioView(MensajeroRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        servicio = Servicio.servicios_cliente.get_servicio_actual(request.user)
        if not servicio:
            return render(request, 'usuarios/indexMensajero.html')  
        form = ServicioEstadoForm(instance=servicio)
        return render(request, 'servicios/gestionarServicioMensajero.html', {'form': form, 'servicio': servicio})
    
    def post(self, request, *args, **kwargs):
        servicio = Servicio.servicios_cliente.get_servicio_actual(request.user)
        if not servicio:
            return render(request, 'usuarios/indexMensajero.html')  

        form = ServicioEstadoForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('gestionarServicio')

        return render(request, 'servicios/gestionarServicioMensajero.html', {'form': form, 'servicio': servicio})
    


class CompletarServicioView(MensajeroRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        servicio = Servicio.servicios_cliente.get_servicio_actual(request.user)
        if not servicio:
            return render(request, 'servicios/no_servicio.html')  

        servicio.is_complete = True
        servicio.estados = 'E'
        servicio.save()

        return redirect('gestionarServicio')
    


class HistorialServiciosMensajeroView(TemplateView, MensajeroRequiredMixin):
    template_name = "servicios/historialMensajero.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        historial = Servicio.servicios_cliente.get_historial_servicios_mensajeros(self.request.user)
        print(historial)
        context['historial'] = historial
        return context
    

class HistorialServiciosClienteView(TemplateView, ClienteRequiredMixin):
    template_name = "servicios/historialCliente.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        historial = Servicio.servicios_cliente.get_historial_servicios_cliente(self.request.user)
        print(historial)
        context['historial'] = historial
        return context



class ServicioListView(ListView):
    model = Servicio
    template_name = "Admin/listarServiciosAdmin.html"
    context_object_name = 'servicios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ServicioFilterForm(self.request.GET)
        if form.is_valid():

            ciudad_ida = form.cleaned_data.get('ciudad_ida')
            if ciudad_ida:
                queryset = queryset.filter(direccion_recojer__ciudad=ciudad_ida)
                print(ciudad_ida)
                print(queryset)

            ciudad_llegada = self.request.GET.get('ciudad_llegada')
            if ciudad_llegada:
                queryset = queryset.filter(direccion_destino__ciudad=ciudad_llegada)
                

            is_complete = self.request.GET.get('is_complete')
            if is_complete:
                queryset = queryset.filter(is_complete = True)

            fecha_creacion = self.request.GET.get('fecha_creacion')
            if fecha_creacion:
                print(fecha_creacion)
                fecha_creacion = make_aware(datetime.strptime(fecha_creacion, '%Y-%m-%d'))
                queryset = queryset.filter(fecha_creacion__gte = fecha_creacion)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServicioFilterForm(self.request.GET or None)  # Instancia el formulario
        return context
    


def generar_reporte(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_envios.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, height - 30, "Reporte de Envíos")

    p.setFont("Helvetica", 12)
    p.drawString(30, height - 60, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")

    # Ciudades con más llegadas de envíos
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, height - 90, "Ciudades con más llegadas de envíos:")

    y = height - 110
    for ciudad in Servicio.servicios_cliente.get_ciudades_con_mas_envios():
        p.setFont("Helvetica", 12)
        p.drawString(30, y, f"{ciudad['direccion_destino__ciudad']}: {ciudad['total']} envíos")
        y -= 20

    # Usuarios con más envíos asociados
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, y - 20, "Usuarios con más envíos asociados:")

    y -= 40
    for usuario in Servicio.servicios_cliente.get_usuarios_con_mas_envios():
        p.setFont("Helvetica", 12)
        p.drawString(30, y, f"{usuario['id_cliente__username']}: {usuario['total_envios']} envíos")
        y -= 20


    p.showPage()
    p.save()

    return response