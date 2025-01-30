from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal import RepositorioDeReporteMunicipal


class ServicioReporteMunicipal():
    """
    Servicio que gestiona la lógica de negocio de los reportes municipales.
    """

    def __init__(self, repositorio_reporte: RepositorioDeReporteMunicipal):
        self.repositorio_reporte = repositorio_reporte

    def obtener_reportes_municipales(self):
        """
        Obtiene todos los reportes municipales.

        :return: Lista de todos los reportes municipales.
        """
        return self.repositorio_reporte.obtener_todos()

    def obtener_reporte_municipal_por_id(self, id_reporte):
        """
        Obtiene un reporte municipal por su ID.

        :param id_reporte: ID del reporte municipal.
        :return: Instancia de ReporteMunicipal o None si no existe.
        """
        return self.repositorio_reporte.obtener_por_id(id_reporte)


    def atender_reporte_municipal(self, reporte):
        """
        Marca un reporte como 'atendiendo'.

        """
        if reporte:
            reporte.cambiar_estado("atendiendo")
            return True
        return False

    def postergar_reporte(self, reporte):
        """
        Marca un reporte como 'postergado'.

        """
        if reporte:
            reporte.cambiar_estado("postergado")
            return True
        return False

    def registrar_evidencia(self, reporte, descripcion_evidencia):
        if reporte:
            reporte.registrar_evidencia(descripcion_evidencia)
        return reporte

