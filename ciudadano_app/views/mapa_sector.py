from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from shared.models.sector import Sector  # Actualizar si existe

@login_required
def ver_mapa_sector(request, nombre_sector):
    # Decodificar el nombre del sector de la URL
    nombre_sector = unquote(nombre_sector)
    
    # Coordenadas aproximadas de los sectores de Quito
    coordenadas_sectores = {
        'BELISARIO QUEVEDO': [-0.1897, -78.4982],
        'EL INCA': [-0.1547, -78.4778],
        'CARCELÉN': [-0.0947, -78.4778],
        'CENTRO HISTÓRICO': [-0.2201, -78.5123],
        'CHILIBULO': [-0.2447, -78.5323],
        'CHILLOGALLO': [-0.2847, -78.5523],
        'CHIMBACALLE': [-0.2501, -78.5123],
        'COCHAPAMBA': [-0.1447, -78.4978],
        'COMITÉ DEL PUEBLO': [-0.1247, -78.4678],
        'CONCEPCIÓN': [-0.1647, -78.4878],
        'COTOCOLLAO': [-0.1147, -78.4878],
        'EL CONDADO': [-0.1047, -78.4978],
        'MAGDALENA': [-0.2447, -78.5223],
        'GUAMANÍ': [-0.3247, -78.5523],
        'IÑAQUITO': [-0.1747, -78.4878],
        'ITCHIMBÍA': [-0.2147, -78.5023],
        'JIPIJAPA': [-0.1647, -78.4778],
        'KENNEDY': [-0.1447, -78.4778],
        'LA ARGELIA': [-0.2647, -78.5023],
        'LA ECUATORIANA': [-0.3047, -78.5523],
        'LA FERROVIARIA': [-0.2547, -78.5223],
        'LA LIBERTAD': [-0.2247, -78.5223],
        'LA MENA': [-0.2647, -78.5423],
        'MARISCAL SUCRE': [-0.2047, -78.4923],
        'PONCEANO': [-0.1247, -78.4778],
        'PUENGASÍ': [-0.2447, -78.4923],
        'QUITUMBE': [-0.2847, -78.5423],
        'RUMIPAMBA': [-0.1847, -78.4923],
        'SAN BARTOLO': [-0.2647, -78.5223],
        'SAN JUAN': [-0.2147, -78.5123],
        'SOLANDA': [-0.2647, -78.5223],
        'TURUBAMBA': [-0.3147, -78.5423],
    }
    
    # Obtener coordenadas del sector o usar coordenadas por defecto de Quito
    coordenadas = coordenadas_sectores.get(nombre_sector.upper(), [-0.2201, -78.5123])
    
    return render(request, 'mapa/ver_sector.html', {
        'nombre_sector': nombre_sector,
        'latitud': coordenadas[0],
        'longitud': coordenadas[1]
    }) 