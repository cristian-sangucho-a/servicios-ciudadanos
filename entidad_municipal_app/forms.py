from django import forms

class EntidadLoginForm(forms.Form):
    correo_electronico = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded'})
    )
