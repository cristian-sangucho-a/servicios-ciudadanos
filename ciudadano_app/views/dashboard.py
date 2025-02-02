from django.shortcuts import render
from ..decorators import ciudadano_required

@ciudadano_required
def dashboard_ciudadano(request):
    return render(request, 'dashboard.html')
