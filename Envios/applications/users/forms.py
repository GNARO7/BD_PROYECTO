from django import forms
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as gl


class ClienteForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}),
    )
    class Meta:
        model = Usuario
        fields = [
            'username', 'nombres', 'apellidos', 'direccion', 'email', 'telefono', 'identificacion', 'ciudad', 
            'nombreSucursal', 'telefonoSucursal', 'address_sucursal', 'password','confirm_password', 'imagenPerfil'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(),
            
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        img = cleaned_data.get("imagenPerfil")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las Contraseñas no coinciden")
        if not img:
            raise forms.ValidationError("Ingrese una imagen de perfil.")
    
    
    
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_cliente = True
        if commit:
            user.save()
        return user

class MensajeroForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}),
    )
    class Meta:
        model = Usuario
        fields = [
            'username','nombres', 'apellidos', 'direccion', 'email', 'telefono', 'identificacion', 'ciudad', 'vehiculo', 
            'placaVehiculo', 'password', 'confirm_password', 'imagenPerfil'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'placaVehiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'imagenPerfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        img = cleaned_data.get("imagenPerfil")

        if password != confirm_password:
            raise forms.ValidationError("Las Contraseñas no coinciden")
        if not img:
            raise forms.ValidationError("Ingrese una imagen de perfil.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_mensajero = True
        if commit:
            user.save()
        return user





class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        label=gl("Nombre de usuario")
    )
    password = forms.CharField(
        label=gl("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['direccion', 'email', 'telefono', 'imagenPerfil']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            
            
        }

    def clean(self):
        cleaned_data = super().clean()
        direccion = cleaned_data.get("direccion")
        email = cleaned_data.get("email")
        telefono = cleaned_data.get("telefono")
        imagenPerfil = cleaned_data.get("imagenPerfil")
        if not direccion:
            raise forms.ValidationError("Ingresa una direccion.")
        if not email:
            raise forms.ValidationError("Ingresa un email.")
        if not telefono:
            raise forms.ValidationError("Ingresa un telefono.")



class UsuarioFilterForm(forms.Form):
    TIPO_CHOICES = (
        ('', 'Todos'),
        ('C', 'Cliente'),
        ('M', 'Mensajero'),
    )
    
    CIUDAD_CHOICES = (
        ('', 'Todas'),
        ('C', 'Santiago de Cali'),
        ('B', 'Bogota'),
        ('M', 'Medellin'),
        ('P', 'Pereira'),
    )

    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False, label="Tipo de Usuario")
    ciudad = forms.ChoiceField(choices=CIUDAD_CHOICES, required=False, label="Ciudad")
        
        
        

        

        