from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from entidad_municipal_app.models import EntidadMunicipal
from django.contrib import admin
from django import forms
from django.contrib.auth.hashers import make_password
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico, EventoMunicipal, RegistroAsistencia

# Custom form to ensure password hashing
class EntidadMunicipalAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=False)

    class Meta:
        model = EntidadMunicipal
        fields = '__all__'

    def clean_password(self):
        """Ensure the password is always hashed before saving"""
        password = self.cleaned_data.get("password")
        if password:
            return make_password(password)  # Hash the password before saving
        return None  # Prevent saving an empty password

# Custom admin configuration for EntidadMunicipal
class EntidadMunicipalAdmin(UserAdmin):
    form = EntidadMunicipalAdminForm
    model = EntidadMunicipal

    list_display = ('correo_electronico', 'nombre', 'direccion', 'telefono', 'is_active', 'is_staff')
    search_fields = ('correo_electronico', 'nombre')
    ordering = ('correo_electronico',)  # Fixed ordering: replaced 'username' with 'correo_electronico'

    fieldsets = (
        (None, {'fields': ('correo_electronico', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'direccion', 'telefono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),  # Added groups and user_permissions
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo_electronico', 'nombre', 'direccion', 'telefono', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    list_filter = ('is_active', 'is_staff')  # Removed 'is_superuser'

admin.site.register(EntidadMunicipal, EntidadMunicipalAdmin)

@admin.register(EspacioPublico)
class EspacioPublicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entidad_municipal')  # entidad_municipal debe ser una relación válida
