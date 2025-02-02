from django import forms
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
    """
    Formulario para crear una nueva reserva.
    """
    TIPO_RESERVA_CHOICES = [
        ('publico', 'Público'),
        ('privado', 'Privado'),
    ]

    tipo_reserva = forms.ChoiceField(
        choices=TIPO_RESERVA_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded', 'id':'tipo_reserva'})
    )

    class Meta:
        model = Reserva
        fields = ['fecha_reserva', 'hora_inicio', 'hora_fin', 'tipo_reserva', 'correos_invitados', 'estado_reserva', 'ciudadano', 'area_comunal']
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'class': 'w-full p-2 border rounded', 'type': 'date', 'readonly': 'readonly'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'w-full p-2 border rounded', 'type': 'time', 'readonly': 'readonly'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'w-full p-2 border rounded', 'type': 'time', 'readonly': 'readonly'}),
            'correos_invitados': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'style': 'display:none;', 'id': 'correos_invitados'}),
            'estado_reserva': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'style': 'display:none;'}),
            'ciudadano': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'area_comunal': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

    def save(self, commit=True):
        reserva = super().save(commit=False)
        servicio_reserva = ServicioReserva()
        id_reserva = None
        fue_reservado = False
        if reserva.tipo_reserva == 'privado':
            id_reserva, fue_reservado = servicio_reserva.reservar_area_comunal_para_actividad_privada(
                reserva.area_comunal,
                reserva.fecha_reserva,
                reserva.hora_inicio,
                reserva.hora_fin,
                reserva.tipo_reserva,
                reserva.ciudadano,
                reserva.correos_invitados
            )
        id_reserva, fue_reservado = servicio_reserva.reservar_area_comunal(
            reserva.area_comunal,
            reserva.fecha_reserva,
            reserva.hora_inicio,
            reserva.hora_fin,
            reserva.tipo_reserva,
            reserva.ciudadano
        )
        if not fue_reservado:
            raise ValidationError("No se pudo realizar la reserva.")
        if commit:
            reserva.save()
        return reserva