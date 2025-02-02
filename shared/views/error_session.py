from django.shortcuts import render

def error_session(request):
    return render(request, 'error_session.html')
