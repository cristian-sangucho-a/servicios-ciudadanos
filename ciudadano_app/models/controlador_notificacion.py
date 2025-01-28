import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ciudadano_app.models import Reserva


class ControladorNotificacion():

    def enviar_invitacion(self, reserva: Reserva):
        usuario = reserva.ciudadano.nombre_completo
        asunto = "Invitación a actividad grupal de tipo privada"
        destinatarios = reserva.correos_invitados.split(',')
        mensaje = "Buen día. Usted ha sido invitado a una actividad grupal en: " + reserva.obtener_area_comunal()+". La actividad se llevará a cabo el día: "+reserva.fecha_reserva+" de "+reserva.hora_inicio+" a "+reserva.hora_fin+"."
        emailSource = 'serviciosciudadanos2@gmail.com'
        password = 'tpbc jstj tlpv nalo'  # Contraseña de aplicación

        # Crear la instancia del objeto mensaje
        msg = MIMEMultipart()
        msg['From'] = f'{usuario} <{emailSource}>'
        msg['To'] = ', '.join(destinatarios)
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'plain'))

        # Envío del correo
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()  # Identificación inicial
                server.starttls()  # Iniciar conexión segura
                server.ehlo()
                server.login(emailSource, password)  # Autenticación
                server.sendmail(emailSource, destinatarios, msg.as_string())
                return True
        except smtplib.SMTPAuthenticationError:
            return False
        except Exception as e:
            return False