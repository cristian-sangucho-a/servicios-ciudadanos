from django.shortcuts import render

def cargar_calendario(request):
    area_id = request.GET.get('area_id')
    return render(request, 'calendario_area.html', {
        'area_id': area_id
    })

