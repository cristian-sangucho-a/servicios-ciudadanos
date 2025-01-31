from django import forms
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from django.core.exceptions import ValidationError

class CiudadanoLoginForm(forms.Form):
    correo_electronico = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'})
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
