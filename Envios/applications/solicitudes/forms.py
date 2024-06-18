from django import forms
from .models import Direccion, Servicio
from applications.users.models import Usuario  
from datetime import datetime

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['direccion', 'ciudad', 'departamento', 'codigo_postal', 'pais']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),   
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['descripcion', 'vehiculoSolicitado']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculoSolicitado': forms.Select(attrs={'class': 'form-control'}),   
        }

class ServicioEstadoForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['estados', 'imagenEstado']
        widgets = {
            'estados': forms.Select(attrs={'class': 'form-control'}),   
            'imagenEstado': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        servicio = super().save(commit=False)
        
        if self.cleaned_data.get('imagenEstado'):
            servicio.imagenEstado = self.cleaned_data['imagenEstado']
        else:
            if self.instance.pk:
                previous_instance = Servicio.objects.get(pk=self.instance.pk)
                servicio.imagenEstado = previous_instance.imagenEstado
        
        if commit:
            servicio.save()
        
        return servicio
    

class ServicioFilterForm(forms.Form):
    CIUDAD_CHOICES = (
        ('', 'Todas...'),
        ('C','Santiago de Cali'),
        ('B','Bogota'),
        ('M','Medellin'),
        ('P','Pereira'),
    )

    is_complete = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ciudad_ida = forms.ChoiceField(choices=CIUDAD_CHOICES, required=False)
    ciudad_llegada = forms.ChoiceField(choices=CIUDAD_CHOICES, required=False)
    fecha_creacion = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


