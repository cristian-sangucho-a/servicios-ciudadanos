from django.core.exceptions import ObjectDoesNotExist

from entidad_municipal_app.models import EventoMunicipal


class RepositorioEventos:
    """
    Repositorio para gestionar las operaciones relacionadas con los eventos municipales.
    """

    def obtener_evento_por_id(self, evento_id):
        """
        Obtiene un evento por su ID.

        Args:
            evento_id (int): El ID del evento.

        Returns:
            EventoMunicipal: El evento encontrado.

        Raises:
            ObjectDoesNotExist: Si el evento no existe.
        """
        try:
            return EventoMunicipal.objects.get(pk=evento_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"El evento con ID {evento_id} no existe.")


    def actualizar_evento(self, evento_id, **kwargs):
        """
        Actualiza un evento existente.

        Args:
            evento_id (int): El ID del evento a actualizar.
            **kwargs: Campos a actualizar.

        Returns:
            EventoMunicipal: El evento actualizado.

        Raises:
            ObjectDoesNotExist: Si el evento no existe.
        """
        evento = self.obtener_evento_por_id(evento_id)
        for key, value in kwargs.items():
            setattr(evento, key, value)
        evento.save()
        return evento


    def cancelar_evento(self, evento_id, motivo):
        """
        Cancela un evento y actualiza el motivo de cancelación.

        Args:
            evento_id (int): El ID del evento a cancelar.
            motivo (str): El motivo de la cancelación.

        Returns:
            EventoMunicipal: El evento cancelado.

        Raises:
            ObjectDoesNotExist: Si el evento no existe.
        """
        evento = self.obtener_evento_por_id(evento_id)
        evento.estado_actual = EventoMunicipal.ESTADO_CANCELADO
        evento.set_motivo_cancelacion(motivo)
        evento.save()
        return evento

    def listar_eventos_programados(self):
        """
        Obtiene una lista de todos los eventos programados.

        Returns:
            QuerySet: QuerySet de eventos programados.
        """
        return EventoMunicipal.objects.filter(estado_actual=EventoMunicipal.ESTADO_PROGRAMADO)

    def listar_eventos_en_curso(self):
        """
        Obtiene una lista de todos los eventos en curso.

        Returns:
            QuerySet: QuerySet de eventos en curso.
        """
        return EventoMunicipal.objects.filter(estado_actual=EventoMunicipal.ESTADO_EN_CURSO)

    def listar_eventos_finalizados(self):
        """
        Obtiene una lista de todos los eventos finalizados.

        Returns:
            QuerySet: QuerySet de eventos finalizados.
        """
        return EventoMunicipal.objects.filter(estado_actual=EventoMunicipal.ESTADO_FINALIZADO)

    def listar_eventos_cancelados(self):
        """
        Obtiene una lista de todos los eventos cancelados.

        Returns:
            QuerySet: QuerySet de eventos cancelados.
        """
        return EventoMunicipal.objects.filter(estado_actual=EventoMunicipal.ESTADO_CANCELADO)

    def listar_eventos_programados_por_entidad(self, entidad_municipal):
        """
        Obtiene una lista de todos los eventos programados de una entidad municipal.

        Args:
            entidad_municipal (EntidadMunicipal): La entidad municipal.

        Returns:
            QuerySet: QuerySet de eventos programados.
        """
        return EventoMunicipal.objects.filter(
            estado_actual=EventoMunicipal.ESTADO_PROGRAMADO,
            entidad_municipal=entidad_municipal
        )

    def listar_eventos_en_curso_por_entidad(self, entidad_municipal):
        """
        Obtiene una lista de todos los eventos en curso de una entidad municipal.

        Args:
            entidad_municipal (EntidadMunicipal): La entidad municipal.

        Returns:
            QuerySet: QuerySet de eventos en curso.
        """
        return EventoMunicipal.objects.filter(
            estado_actual=EventoMunicipal.ESTADO_EN_CURSO,
            entidad_municipal=entidad_municipal
        )

    def listar_todos_los_eventos_por_entidad(self, entidad_municipal):
            eventos = EventoMunicipal.objects.filter(
                entidad_municipal=entidad_municipal
            )
            if eventos.exists():
                return eventos
            else:
                return "No se encontraron eventos."
