from datetime import datetime

from django import forms

from ciudadano_app.models import AreaComunal
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from django.core.exceptions import ValidationError

from ciudadano_app.models.reserva.reserva import Reserva
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


class CiudadanoLoginForm(forms.Form):
    correo_electronico = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded'})
    )


class CiudadanoRegisterForm(forms.ModelForm):
    """
    Formulario para registrar un nuevo ciudadano.
    """
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'})
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'})
    )

    class Meta:
        model = Ciudadano
        fields = ['correo_electronico', 'nombre_completo', 'numero_identificacion']
        widgets = {
            'correo_electronico': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        ciudadano = super().save(commit=False)
        password = self.cleaned_data["password"]
        ciudadano.set_password(password)  # Encripta la contraseña
        if commit:
            ciudadano.save()
        return ciudadano

class ReservaRegisterForm(forms.ModelForm):
    TIPO_RESERVA_CHOICES = [
        ('publico', 'Público'),
        ('privado', 'Privado'),
    ]

    tipo_reserva = forms.ChoiceField(
        choices=TIPO_RESERVA_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'})
    )

    correos_invitados = forms.CharField(
        required=False,  # Hacemos el campo no requerido por defecto
        widget=forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 2})
    )

    class Meta:
        model = Reserva
        fields = [
            'fecha_reserva',
            'hora_inicio',
            'hora_fin',
            'tipo_reserva',
            'correos_invitados',  # Campo condicional
            'estado_reserva',
            'ciudadano',
            'area_comunal'
        ]
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date', 'readonly': True}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'readonly': True}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'readonly': True}),
            'estado_reserva': forms.HiddenInput(),
            'ciudadano': forms.HiddenInput(),
            'area_comunal': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        fecha = cleaned_data.get('fecha_reserva')
        if fecha and fecha < datetime.now().date():
            self.add_error('fecha_reserva', 'No puedes reservar_area_comunal en fechas pasadas')

        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            self.add_error('hora_fin', 'La hora final debe ser posterior a la inicial')

        tipo_reserva = cleaned_data.get('tipo_reserva')
        correos_invitados = cleaned_data.get('correos_invitados')

        if tipo_reserva == 'privado' and not correos_invitados:
            self.add_error('correos_invitados', 'Los correos son obligatorios para reservas privadas')
        elif tipo_reserva == 'publico':
            cleaned_data['correos_invitados'] = ''

        return cleaned_data

    def save(self, commit = ...):
        reserva = super().save(commit=False)
        reserva.estado_reserva = 'Activa'
        if commit:
            reserva.save()
        return reserva