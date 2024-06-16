from django.shortcuts import render
from .models import *
from .forms import ClienteForm, MensajeroForm, CustomLoginForm, UpdateUserForm, UsuarioFilterForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

# Create your views here.


class MensajeroCreateView(CreateView):
    model = Usuario
    form_class = MensajeroForm
    template_name = 'usuarios/crearMensajero.html'
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        print(form.cleaned_data)
        response = super().form_valid(form)
        return response
    

class ClienteCreateView(CreateView):
    model = Usuario
    form_class = ClienteForm
    template_name = 'usuarios/crearCliente.html'
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_cliente:
            return reverse_lazy('indexCliente')  
        elif user.is_mensajero:
            return reverse_lazy('indexMensajero')
        elif user.is_staff:
            return reverse_lazy('indexAdmin')  
        else:
            return reverse_lazy('default_dashboard')  




# class indexMensajero(TemplateView):
#     template_name = "usuarios/indexMensajero.html"


# class indexCliente(TemplateView):
#     template_name = "usuarios/indexCliente.html"



class ClienteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_cliente

class MensajeroRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_mensajero
    
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class PrincipalClienteView(ClienteRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usuarios/indexCliente.html')
    

class PrincipalMensajeroView(MensajeroRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usuarios/indexMensajero.html')


#view para el index principal
def home(request):
    return render(request, 'home/home.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))




class UserUpdateView(UpdateView):
    model = Usuario
    template_name = "usuarios/actualizarUser.html"
    form_class =  UpdateUserForm
    success_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('login')



class UsuarioListView(ListView, AdminRequiredMixin):
    model = Usuario
    template_name = 'Admin/listarUsuariosAdmin.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        queryset = Usuario.objects.all()
        form = UsuarioFilterForm(self.request.GET)
        if form.is_valid():
            tipo = form.cleaned_data.get('tipo')
            ciudad = form.cleaned_data.get('ciudad')
            if tipo == 'C':
                queryset = queryset.filter(is_cliente=True)
            elif tipo == 'M':
                queryset = queryset.filter(is_mensajero=True)
            if ciudad:
                queryset = queryset.filter(ciudad=ciudad)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = UsuarioFilterForm(self.request.GET)
        return context
    

