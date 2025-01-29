from django.db import models

from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.reporte.reporte_municipal import ReporteMunicipal


class GestorDeDepartamentosYReportes(models.Model):
    """
    Clase de gestión que maneja el CRUD de Reportes Municipales y Departamentos.

    Métodos:
        ReporteMunicipal:
            - crear_reporte_municipal()
            - obtener_reportes_municipales()
            - obtener_reporte_municipal_por_id()
            - actualizar_reporte_municipal()
            - eliminar_reporte_municipal()

        Departamento:
            - crear_departamento()
            - obtener_departamentos()
            - obtener_departamento_por_nombre()
            - actualizar_departamento()
            - eliminar_departamento()
    """

    # ReporteMunicipal

    @staticmethod
    def obtener_reportes_municipales():
        """
        Obtiene todos los reportes municipales.

        :return: QuerySet de ReporteMunicipal.
        :rtype: QuerySet[ReporteMunicipal]
        """
        return ReporteMunicipal.objects.all()

    @staticmethod
    def obtener_reporte_municipal_por_id(id_reporte):
        """
        Obtiene un reporte municipal por su ID.

        :param id_reporte: ID del reporte municipal.
        :type id_reporte: int
        :return: Instancia de ReporteMunicipal o None si no existe.
        :rtype: ReporteMunicipal | None
        """
        return ReporteMunicipal.objects.filter(id=id_reporte).first()

    @staticmethod
    def eliminar_reporte_municipal(id_reporte):
        """
        Elimina un reporte municipal.

        :param id_reporte: ID del reporte a eliminar.
        :type id_reporte: int
        :return: True si se eliminó correctamente, False si no existía.
        :rtype: bool
        """
        reporte = ReporteMunicipal.objects.filter(id=id_reporte).first()
        if reporte:
            reporte.delete()
            return True
        return False

    # **🔹 CRUD de Departamento**

    @staticmethod
    def obtener_departamentos():
        """
        Obtiene todos los departamentos registrados.

        :return: QuerySet de Departamento.
        :rtype: QuerySet[Departamento]
        """
        return Departamento.objects.all()

    @staticmethod
    def obtener_departamento_por_nombre(nombre):
        """
        Obtiene un departamento por su nombre.

        :param nombre: Nombre del departamento a buscar.
        :type nombre: str
        :return: Instancia de Departamento o None si no existe.
        :rtype: Departamento | None
        """
        return Departamento.objects.filter(nombre__iexact=nombre).first()


    def atender_reporte_municipal(self, reporte:ReporteMunicipal):
        """
        Marca un reporte como 'atendiendo'.

        :param reporte: Instancia de ReporteMunicipal.
        :type reporte: ReporteMunicipal
        """
        reporte = self.obtener_reporte_municipal_por_id()
        reporte.cambiar_estado("atendiendo")
        reporte.save()

    def postergar_reporte(self, reporte:ReporteMunicipal):
        """
        Marca un reporte como 'postergado'.

        :param reporte: Instancia de ReporteMunicipal.
        :type reporte: ReporteMunicipal
        """
        reporte.cambiar_estado("postergado")
        reporte.save()
