from app.Departamento import Departamento


class GestorDeDepartamentos:
    def __init__(self):
        # Lista de reportes no asignados
        self.__reportes_no_asignados = []

        # Lista de departamentos predefinidos
        self.__departamentos = [
            Departamento('EPMMOP'),
            Departamento('AMT'),
            Departamento('EMASEO')
        ]

        # Clasificaciones de los departamentos
        self.__departamentos_clasificacion = {
            'EPMMOP': [
                'hueco', 'calle', 'asfalto', 'paso cebra',
                'EPMMOP', 'bache', 'puente', 'vía', 'acera', 'semáforo',
                'infraestructura', 'drenaje', 'reparación vial',
                'construcción', 'mantenimiento'
            ],
            'AMT': [
                'choque', 'congestionamiento', 'vehículo', 'accidente',
                'señalización', 'parqueo', 'patrullaje', 'control vehicular',
                'revisión técnica', 'zona azul'
            ],
            'EMASEO': [
                'basura', 'residuos', 'reciclaje', 'limpieza',
                'acumulación de desechos', 'recolección', 'contenedores',
                'desechos sólidos', 'escombros', 'saneamiento'
            ]
        }

    def agregar_nuevo_reporte_no_asignado(self, reporte):
        """Agrega un reporte a la lista de reportes no asignados."""
        self.__reportes_no_asignados.append(reporte)

    def obtener_reportes_no_asignados(self):
        """Devuelve la lista de reportes no asignados."""
        return self.__reportes_no_asignados

    def __obtener_numero_coincidencias(self, descripcion, keywords):
        """
        Devuelve el número de coincidencias entre las palabras de la descripción y las palabras clave
        :param descripcion: Descripción del reporte
        :param keywords: Lista de palabras clave del departamento
        :return: Nivel de confianza como porcentaje (0-100)
        """
        descripcion_palabras = descripcion.split()
        numero_coincidencias_palabras = sum(1 for palabra in descripcion_palabras if palabra in keywords)
        if len(descripcion_palabras) == 0:
            return 0
        return numero_coincidencias_palabras

    def __encontrar_departamento_por_clasificacion(self, reporte):
        """
        Encuentra el nombre del departamento con mas palabras clave
        :param reporte: Reporte a clasificar
        :return: Departamento con mayor nivel de confianza, si supera el umbral, o None
        """
        descripcion = reporte.obtener_descripcion().lower()
        numero_max = 0
        nombre_departamento_seleccionado = ""

        for nombre_departamento_actual, keywords in self.__departamentos_clasificacion.items():
            numero_coincidencias = self.__obtener_numero_coincidencias(descripcion, keywords)
            if numero_coincidencias > numero_max:
                numero_max = numero_coincidencias
                nombre_departamento_seleccionado = nombre_departamento_actual

        return nombre_departamento_seleccionado

    def asignar_automaticamente_reportes_a_departamentos(self):
        for reporte in self.__reportes_no_asignados[:]:
            nombre_departamento = self.__encontrar_departamento_por_clasificacion(reporte)

            if nombre_departamento:
                departamento = self.obtener_departamento_por_nombre(nombre_departamento)

                if not departamento:
                    self.agregar_departamento(Departamento(nombre_departamento))

                departamento.agregar_reporte(reporte)
                self.__reportes_no_asignados.remove(reporte)


    def obtener_departamento_por_nombre(self, nombre):
        """Devuelve un departamento por su nombre."""
        for departamento in self.__departamentos:
            if departamento.obtener_nombre().lower() == nombre.lower():
                return departamento
        return None

    def agregar_departamento(self, departamento):
        """Agrega un nuevo departamento a la lista."""
        self.__departamentos.append(departamento)

    def asignar_manualmente_reporte_a_departamento(self, reporte, departamento):
        """Asigna un reporte a un departamento de forma manual."""
        departamento.agregar_reporte(reporte)
        if reporte in self.__reportes_no_asignados:
            self.__reportes_no_asignados.remove(reporte)

    def agregar_criterios_clasificacion_por_departamento(self, departamento, criterios):
        """Añade criterios de clasificación a un departamento específico."""
        if departamento.obtener_nombre() in self.__departamentos_clasificacion:
            self.__departamentos_clasificacion[departamento.obtener_nombre()].extend(criterios)
        else:
            self.__departamentos_clasificacion[departamento.obtener_nombre()] = criterios

    def obtener_criterios_clasificacion_por_departamento(self, departamento):
        """Devuelve los criterios de clasificación de un departamento."""
        return self.__departamentos_clasificacion.get(departamento.obtener_nombre(), [])

    def obtener_reporte_por_id(self, id_reporte):
        for reporte in self.__reportes_no_asignados:
            if reporte.obtener_id() == id_reporte:
                return reporte
        return None