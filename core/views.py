from django.shortcuts import render

def landing_page(request):
    """
    Vista para la página principal (landing page) del sitio.
    """
    return render(request, 'landing_page.html')
