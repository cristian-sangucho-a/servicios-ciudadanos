class ServicioDeNotificacion:
    def notificar(self, ciudadano, mensaje):
        # Simulación de envío de correo
        print(f"Enviando correo a {ciudadano.nombre}: {mensaje}")
        ciudadano.get_notificacion.append(mensaje)