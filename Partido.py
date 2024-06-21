class Partido:
    def __init__(self, equipo_local, equipo_visitante, estadio, dia, hora):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.estadio = estadio
        self.dia = dia
        self.hora = hora
        self.resultado = None

    def jugar_partido(self, resultado):
        self.resultado = resultado

    def mostrar_resultado(self):
        if self.resultado:
            return f"Partido en {self.estadio.nombre} - {self.equipo_local.nombre} vs {self.equipo_visitante.nombre}: {self.resultado}"
        else:
            return f"Partido en {self.estadio.nombre} - {self.equipo_local.nombre} vs {self.equipo_visitante.nombre}: Aún no jugado"

    def mostrar_info(self):
        return f"Partido: {self.equipo_local.nombre} vs {self.equipo_visitante.nombre}\n" \
               f"Estadio: {self.estadio.nombre}\nCiudad: {self.estadio.ciudad}\nCapacidad: {self.estadio.capacidad}\n" \
               f"Día: {self.dia}\nHora: {self.hora}"
